# -*- coding: utf-8 -*-
from contextlib import contextmanager

from django.conf import settings
from django.db import connections
from django.utils.functional import Promise

from etools_datamart.state import state


class RawSql(str):
    """
    A str subclass that has been specifically marked as "raw"
    skip any tenant related manipulation
    """

    def __add__(self, rhs):
        """
        Concatenating a raw string with another string
        Otherwise, the result is no longer safe.
        """
        t = super().__add__(rhs)
        if isinstance(rhs, RawSql):
            return RawSql(t)
        return t

    def __str__(self):
        return self


def raw_sql(s):
    """
    Explicitly mark a string as raw sql. The returned
    object can be used everywhere a string is appropriate.

    Can be called multiple times on a single string.
    """
    if isinstance(s, (str, Promise)):
        return RawSql(s)
    return RawSql(str(s))


def get_public_schema_name():
    return getattr(settings, 'PUBLIC_SCHEMA_NAME', 'public')


@contextmanager
def current_schema(schema):
    _old = state.schemas
    state.schemas = [schema]
    yield
    state.schemas = _old


@contextmanager
def clear_schemas():
    _old = state.schemas
    state.schemas = []
    yield
    state.schemas = _old


@contextmanager
def single():
    _old = state.schemas
    conn = connections['etools']
    state.schemas = []
    conn.mode = 1
    yield
    state.schemas = _old
    conn.mode = 2
