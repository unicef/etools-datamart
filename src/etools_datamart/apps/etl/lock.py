# -*- coding: utf-8 -*-
import logging
from functools import partial, wraps

from django.core.cache import caches
from redis.exceptions import LockError

cache = caches['default']

logger = logging.getLogger(__name__)

LOCK_EXPIRE = 60 * 60  # Lock expires in 1 hour


class TaskExecutionOverlap(Exception):
    pass


def only_one(function=None, key="", timeout=None):
    """Enforce only one celery task at a time."""

    def _unlock(key):
        try:
            lock = cache.lock(key, timeout=timeout)
            cache.delete(key)
            lock.release()
        except LockError:
            pass

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
                # else:
                #     raise TaskExecutionOverlap(key)
            finally:
                if have_lock:
                    try:
                        lock.release()
                    except LockError as e:  # pragma: no cover
                        logger.warning(e)

            return ret_value

        return _caller
    function.unlock = partial(_unlock, key)
    return _dec(function) if function is not None else _dec
