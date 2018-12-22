# # -*- coding: utf-8 -*-
# import uuid
#
# from etools_datamart.apps.etl.lock import locks, only_one
#
#
# def test_only_one():
#     call = 0
#
#     def func():
#         nonlocal call
#         call += 1
#     key = uuid.uuid4()
#     wrapped = only_one(func, key=key)
#     wrapped()
#     assert call == 1
#     wrapped()
#     assert call == 2
#
#     lock = cache.lock(key)
#     assert lock.acquire(blocking=False)
#
#     wrapped()
#     assert call == 2
#     lock.release()
