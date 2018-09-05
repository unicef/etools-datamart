# -*- coding: utf-8 -*-

import atexit
import json
import logging
import os
import threading
from queue import Queue
from time import sleep, time

from django.utils.timezone import now
from strategy_field.utils import import_by_name
from unicef_rest_framework.utils import get_ident

from etools_datamart.apps.tracking.models import APIRequestLog
from etools_datamart.state import state

logger = logging.getLogger(__name__)


def _get_record(request, response):
    user_id = None
    app_id = None

    if request.user and request.user.is_authenticated():
        user_id = request.user.pk

    # compute response time
    response_timedelta = now() - request.timestamp
    response_ms = int(response_timedelta.total_seconds() * 1000)
    response_length = len(response.content)

    # get POST data
    try:
        data_dict = request.POST.dict()
    except AttributeError:  # if already a dict, can't dictify
        data_dict = request.data

    try:
        media_type = response.accepted_media_type
    except AttributeError:
        media_type = response['Content-Type'].split(';')[0]

    viewset = ''

    # save to log
    from unicef_rest_framework.utils import get_ident
    return dict(user_id=user_id,
                application_id=app_id,
                requested_at=request.timestamp,
                response_ms=response_ms,
                response_length=response_length,
                path=request.path,
                remote_addr=get_ident(request),
                host=request.get_host(),
                method=request.method,
                query_params=json.dumps(request.GET.dict()),
                data=data_dict,
                viewset=viewset,
                cached=state.get('cache-hit', False),  # see api.common.APICacheResponse
                content_type=media_type)


class AsyncLogger(object):
    _terminator = object()

    def __init__(self, shutdown_timeout=10):
        self._queue = Queue(-1)
        self._lock = threading.Lock()
        self._thread = None
        self._thread_for_pid = None
        self.options = {
            'shutdown_timeout': shutdown_timeout,
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
            if not self.is_alive():
                # thread not started or already stopped - nothing to do
                return

            # wake the processing thread up
            self._queue.put_nowait(self._terminator)

            timeout = self.options['shutdown_timeout']

            # wait briefly, initially
            initial_timeout = 0.1
            if timeout < initial_timeout:
                initial_timeout = timeout

            if not self._timed_queue_join(initial_timeout):
                # if that didn't work, wait a bit longer
                # NB that size is an approximation, because other threads may
                # add or remove items
                size = self._queue.qsize()

                print("Logging sub-system is attempting to send %i pending messages"
                      % size)
                print("Waiting up to %s seconds" % timeout)

                if os.name == 'nt':
                    print("Press Ctrl-Break to quit")
                else:
                    print("Press Ctrl-C to quit")

                self._timed_queue_join(timeout - initial_timeout)

            self._thread = None

        finally:
            self._lock.release()

    def _target(self):
        while True:
            record = self._queue.get()
            try:
                if record is self._terminator:
                    break
                try:

                    # FIXME: remove me (print)
                    print(f"111: middleware.py:117 (_target)- {record}")
                    kwargs = _get_record(**record)
                    kwargs['service'] = import_by_name(record['viewset']).get_service()
                    APIRequestLog.objects.create(**kwargs)
                except ValueError:
                    # TODO: remove after fixing the missing 'viewset' in record[]
                    record['service'] = None
                    APIRequestLog.objects.create(**record)
                except Exception:
                    logger.error('Failed processing job', exc_info=True)
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

    def queue(self, **kwargs):
        self._ensure_thread()
        self._queue.put_nowait(kwargs)

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


class StatsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def log(self, request, response):
        try:
            # kwargs['service'] = import_by_name(kwargs['viewset']).get_service()
            kwargs = _get_record(request, response)
            APIRequestLog.objects.create(**kwargs)
        except Exception as e:
            logger.exception(e)

    def log2(self, request, response):
        user_id = None
        app_id = None

        if request.user and request.user.is_authenticated():
            user_id = request.user.pk

        # compute response time
        response_timedelta = now() - request.timestamp
        response_ms = int(response_timedelta.total_seconds() * 1000)
        response_length = len(response.content)

        # get POST data
        try:
            data_dict = request.POST.dict()
        except AttributeError:  # if already a dict, can't dictify
            data_dict = request.data

        try:
            media_type = response.accepted_media_type
        except AttributeError:
            media_type = response['Content-Type'].split(';')[0]

        viewset = ''

        # save to log
        self.log(user_id=user_id,
                 application_id=app_id,
                 requested_at=request.timestamp,
                 response_ms=response_ms,
                 response_length=response_length,
                 path=request.path,
                 remote_addr=get_ident(request),
                 host=request.get_host(),
                 method=request.method,
                 query_params=json.dumps(request.GET.dict()),
                 data=data_dict,
                 viewset=viewset,
                 cached=state.get('cache-hit', False),  # see api.common.APICacheResponse
                 content_type=media_type)

        request.tracked = True

    def __call__(self, request):

        if request.path.startswith('/api/'):
            request.timestamp = now()

        response = self.get_response(request)

        if hasattr(request, 'timestamp') and response.status_code == 200:
            self.log(request, response)
            # user_id = None
            # app_id = None
            # requestor = None
            #
            # if request.user and request.user.is_authenticated():
            #     user_id = request.user.pk
            #
            # # compute response time
            # response_timedelta = now() - request.timestamp
            # response_ms = int(response_timedelta.total_seconds() * 1000)
            # response_length = len(response.content)
            #
            # # get POST data
            # try:
            #     data_dict = request.POST.dict()
            # except AttributeError:  # if already a dict, can't dictify
            #     data_dict = request.data
            #
            # try:
            #     media_type = response.accepted_media_type
            # except:
            #     media_type = response['Content-Type'].split(';')[0]
            #
            # viewset = ''
            #
            # # save to log
            # self.log(user_id=user_id,
            #          application_id=app_id,
            #          requested_at=request.timestamp,
            #          response_ms=response_ms,
            #          response_length=response_length,
            #          path=request.path,
            #          remote_addr=get_ident(request),
            #          host=request.get_host(),
            #          method=request.method,
            #          query_params=json.dumps(request.GET.dict()),
            #          data=data_dict,
            #          viewset=viewset,
            #          cached=state.get('cache-hit', False),  # see api.common.APICacheResponse
            #          content_type=media_type)
            #
            # request.tracked = True
        return response


class ThreadStatsMiddleware(StatsMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response
        self.worker = AsyncLogger()

    def log(self, request, response):
        self.worker.queue(**{'request': request, 'response': response})
    #
    # def log2(self, request, response):
    #     self.worker.queue(**{'request': request, 'response': response})
