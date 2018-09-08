# -*- coding: utf-8 -*-
import logging
from time import sleep

from etools_datamart.apps.tracking.middleware import AsyncLogger

logger = logging.getLogger(__name__)


def test_async(enable_threadstats, monkeypatch):
    class Logger(AsyncLogger):
        TOTAL = 0

        def _process(self, record):
            self.TOTAL += sum(record['data'])

    logger = Logger(shutdown_timeout=2)
    logger.queue(data=[1, 1, 1])
    logger.queue(data=Logger._terminator)
    logger.start()
    sleep(1)
    assert logger.TOTAL == 3
