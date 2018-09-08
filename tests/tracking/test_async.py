# -*- coding: utf-8 -*-
import logging
from time import sleep

from etools_datamart.apps.tracking.middleware import AsyncLogger

logger = logging.getLogger(__name__)


def test_async(enable_threadstats, monkeypatch):
    class Logger(AsyncLogger):
        TOTAL = 0

        def _process(self, record):
            self.TOTAL += sum(record)

    logger = Logger(shutdown_timeout=2)
    logger.queue([1, 1, 1])
    logger.queue(Logger._terminator)
    logger.start()
    sleep(1)
    logger.stop()
    assert logger.TOTAL == 3


def test_async_main_thread_terminated(enable_threadstats, monkeypatch):
    class Logger(AsyncLogger):
        TOTAL = 0

        def _process(self, record):
            self.TOTAL += sum(record)

    logger = Logger(shutdown_timeout=2)
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.start()
    logger.main_thread_terminated()
    assert logger.TOTAL == 12


def test_async_timeout(enable_threadstats, monkeypatch):
    class Logger(AsyncLogger):
        TOTAL = 0

        def _process(self, record):
            self.TOTAL += sum(record)

    logger = Logger(shutdown_timeout=1)
    logger.queue([1, 1, 1])
    sleep(2)
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    assert logger.TOTAL == 3
