# -*- coding: utf-8 -*-
import logging
from functools import wraps

from django.core.cache import caches
from redis.exceptions import LockError

cache = caches['default']

logger = logging.getLogger(__name__)

LOCK_EXPIRE = 60 * 60  # Lock expires in 1 hour


def only_one(function=None, key="", timeout=None):
    """Enforce only one celery task at a time."""

    def _dec(run_func):
        """Decorator."""

        @wraps(run_func)
        def _caller(*args, **kwargs):
            """Caller."""
            ret_value = None
            have_lock = False
            lock = cache.lock(key, timeout=timeout)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    ret_value = run_func(*args, **kwargs)

            finally:
                if have_lock:
                    try:
                        lock.release()
                    except LockError as e:
                        logger.warning(e)

            return ret_value

        return _caller

    return _dec(function) if function is not None else _dec
