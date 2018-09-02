# -*- coding: utf-8 -*-
import logging

import pytest

from etools_datamart.state import State

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.django_db


def test_():
    s = State()
    s.schemas = []
    assert s.schemas == []


def test_clean_empty():
    s = State()
    s.schemas = ['', ' ', 'bolivia', 'chad']
    assert s.schemas == ['bolivia', 'chad']


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
