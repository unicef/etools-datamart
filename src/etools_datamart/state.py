# -*- coding: utf-8 -*-

from threading import local

from django.utils.functional import cached_property

from etools_datamart.apps.multitenant.exceptions import InvalidSchema


class SchemaList(list):
    def __init__(self, iterable=None):
        if iterable:
            iterable = [self._clean(i) for i in map(lambda x: x.lower().strip(), iterable) if i]
        super().__init__(iterable or [])

    def append(self, schema: str):
        schema = self._clean(schema)
        if schema:
            super(SchemaList, self).append(schema)

    def insert(self, index: int, schema: str):
        schema = self._clean(schema)
        if schema:
            super(SchemaList, self).insert(index, schema)

    # def clean(self):
    #     return SchemaList([e for e in self if e])

    def _clean(self, value):
        value = value.lower().strip()

        if value and value not in self.valid:
            raise InvalidSchema(value)
        return value

    @cached_property
    def valid(self):
        from django.db import connections
        return ["public"] + [schema.schema_name for schema in connections['etools'].get_tenants()]


class SchemaDescriptor:
    def __init__(self):
        self.val = SchemaList()

    def __get__(self, instance, owner):
        return self.val

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
