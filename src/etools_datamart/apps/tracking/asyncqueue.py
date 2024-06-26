import atexit
import logging
import os
import threading
from queue import Queue
from time import sleep, time

logger = logging.getLogger(__name__)


class AsyncQueue(object):
    _terminator = object()

    def __init__(self, shutdown_timeout=10):
        self._queue = Queue(-1)
        self._lock = threading.Lock()
        self._thread = None
        self._thread_for_pid = None
        self.options = {
            "shutdown_timeout": shutdown_timeout,
        }
        self.start()

    def is_alive(self):
        if self._thread_for_pid != os.getpid():
            return False
        return self._thread and self._thread.is_alive()

    def _ensure_thread(self):
        if self.is_alive():
            return
        self.start()

    def _timed_queue_join(self, timeout):
        """
        implementation of Queue.join which takes a 'timeout' argument

        returns true on success, false on timeout
        """
        deadline = time() + timeout
        queue = self._queue

        queue.all_tasks_done.acquire()
        try:
            while queue.unfinished_tasks:
                delay = deadline - time()
                if delay <= 0:
                    # timed out
                    return False

                queue.all_tasks_done.wait(timeout=delay)

            return True

        finally:
            queue.all_tasks_done.release()

    def main_thread_terminated(self):
        self._lock.acquire()
        try:
            if not self.is_alive():  # pragma: no cover
                # thread not started or already stopped - nothing to do
                return

            # wake the processing thread up
            self._queue.put_nowait(self._terminator)

            timeout = self.options["shutdown_timeout"]

            # wait briefly, initially
            # initial_timeout = 0.1
            # if timeout < initial_timeout:
            #     initial_timeout = timeout
            initial_timeout = min(timeout, 0.1)

            if not self._timed_queue_join(initial_timeout):
                # if that didn't work, wait a bit longer
                # NB that size is an approximation, because other threads may
                # add or remove items
                size = self._queue.qsize()

                print(f"Logging sub-system is attempting to send {size} pending messages")
                print(f"Waiting up to {timeout} seconds")
                print("Press Ctrl-C to quit")

                self._timed_queue_join(timeout - initial_timeout)

            self._thread = None

        finally:
            self._lock.release()

    def _process(self, record):
        raise NotImplementedError

    def _target(self):
        while True:
            record = self._queue.get()
            try:
                if record is self._terminator:
                    break
                try:
                    self._process(record)
                except Exception:  # pragma: no cover
                    logger.error("Failed processing job", exc_info=True)
            finally:
                self._queue.task_done()

            sleep(0)

    def start(self):
        """
        Starts the task thread.
        """
        self._lock.acquire()
        try:
            if not self.is_alive():
                self._thread = threading.Thread(target=self._target)
                self._thread.setDaemon(True)
                self._thread.start()
                self._thread_for_pid = os.getpid()
        finally:
            self._lock.release()
            atexit.register(self.main_thread_terminated)

    def queue(self, payload):
        self._ensure_thread()
        self._queue.put_nowait(payload)

    def stop(self, timeout=None):
        """
        Stops the task thread. Synchronous!
        """
        self._lock.acquire()
        try:
            if self._thread:
                self._queue.put_nowait(self._terminator)
                self._thread.join(timeout=timeout)
                self._thread = None
                self._thread_for_pid = None
        finally:
            self._lock.release()
