# -*- coding: utf-8 -*-
from contextlib import contextmanager

from etools_datamart.state import state


@contextmanager
def set_schemas(*schemas):
    old = state.schemas
    state.schemas = schemas
    yield
    state.schyemas = old
