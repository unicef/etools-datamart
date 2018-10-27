# -*- coding: utf-8 -*-
import logging
from time import sleep
from unittest.mock import Mock

from etools_datamart.apps.tracking.asyncqueue import AsyncQueue

logger = logging.getLogger(__name__)


class Logger(AsyncQueue):
    TOTAL = 0

    def _process(self, record):
        self.TOTAL += sum(record)


def test_async(enable_threadstats, monkeypatch):
    logger = Logger(shutdown_timeout=2)
    logger.queue([1, 1, 1])
    logger.queue(Logger._terminator)
    logger.start()
    sleep(1)
    logger.stop()
    assert logger.TOTAL == 3


def test_async_main_thread_terminated(enable_threadstats, monkeypatch):
    logger = Logger(shutdown_timeout=2)
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.start()
    logger.main_thread_terminated()
    assert logger.TOTAL == 12


def test_async_timeout(enable_threadstats, monkeypatch):
    monkeypatch.setattr(AsyncQueue, '_timed_queue_join', lambda *args: False)
    # monkeypatch.setattr(AsyncQueue, '_async_timeout', lambda *args: True)

    logger = Logger(shutdown_timeout=0.1)
    logger.queue([1, 1, 1])
    sleep(2)
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.main_thread_terminated()
    assert logger.TOTAL == 12


def test_async_missing_start(enable_threadstats, monkeypatch):
    monkeypatch.setattr(AsyncQueue, 'start', lambda s: False)

    logger = Logger()
    logger.stop()
    assert logger.TOTAL == 0


def test_missing_thread(enable_threadstats, monkeypatch):
    monkeypatch.setattr(AsyncQueue, 'start', lambda s: True)
    logger = Logger()
    logger.queue([1, 1, 1])
    logger.stop()
    assert logger.TOTAL == 0


def test_async__timed_queue_join(enable_threadstats, monkeypatch):
    logger = Logger()
    monkeypatch.setattr(logger, '_queue', Mock(all_tasks_done=Mock(), unfinished_tasks=True), raising=False)

    assert not logger._timed_queue_join(1)
