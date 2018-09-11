# -*- coding: utf-8 -*-
from etools_datamart.apps.etl.lock import cache, only_one


def test_only_one():
    call = 0

    def func():
        nonlocal call
        call += 1

    wrapped = only_one(func, key="abc")
    wrapped()
    assert call == 1
    wrapped()
    assert call == 2

    lock = cache.lock("abc")
    assert lock.acquire(blocking=False)

    wrapped()
    assert call == 2
    lock.release()
