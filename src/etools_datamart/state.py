# -*- coding: utf-8 -*-

from threading import local


class State(local):
    request = None
    schemas = []
    data = {}

    def clear(self):
        self.data = {}
        self.request = None

    def set(self, key, value):
        self.data[key] = value


state = State()
