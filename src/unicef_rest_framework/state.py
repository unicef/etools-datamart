# # -*- coding: utf-8 -*-
#
# from threading import local
#
#
# class State(local):
#     request = None
#     data = {}
#
#     def clear(self):
#         self.data = {}
#         self.request = None
#
#     def set(self, key, value):
#         self.data[key] = value
#
#     def get(self, key, default=None):
#         return self.data.get(key, default)
#
#
# state: State = State()
