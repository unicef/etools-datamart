# -*- coding: utf-8 -*-

from threading import local


class SchemaList(list):

    def append(self, schema: str):
        if schema:
            super(SchemaList, self).append(schema)

    def insert(self, index: int, schema: str):
        super(SchemaList, self).insert(index, schema)

    def clean(self):
        return [e for e in self if e]


class SchemaDescriptor:
    def __init__(self):
        self.val = SchemaList()

    def __get__(self, instance, owner):
        return self.val.clean()

    def __set__(self, instance, value):
        self.val = SchemaList(value)


class State(local):
    request = None
    schemas = SchemaDescriptor()
    data = {}

    def clear(self):
        self.data = {}
        self.request = None

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)


state: State = State()
