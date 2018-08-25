# -*- coding: utf-8 -*-
import logging

from etools_datamart.state import State

logger = logging.getLogger(__name__)


def test_():
    s = State()
    s.schemas = []
    assert s.schemas == []


def test_clean_empty():
    s = State()
    s.schemas = ['', 1, 2]
    assert s.schemas == [1, 2]


def test_append_empty():
    s = State()
    s.schemas = []
    s.schemas.append('')
    assert s.schemas == []


def test_insert_empty():
    s = State()
    s.schemas = []
    s.schemas.append('')
    assert s.schemas == []
