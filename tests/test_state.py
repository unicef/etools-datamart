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


def test_append(monkeypatch):
    s = State()
    monkeypatch.setattr(s.schemas, 'valid', ['bolivia', 'chad', 'zambia'])
    s.schemas = []
    s.schemas.append('bolivia')
    assert s.schemas == ['bolivia']


def test_insert(monkeypatch):
    s = State()
    monkeypatch.setattr(s.schemas, 'valid', ['bolivia', 'chad', 'zambia'])

    s.schemas = []
    s.schemas.insert(0, 'bolivia')
    s.schemas.insert(0, 'chad')
    assert s.schemas == ['chad', 'bolivia']


def test_append_empty():
    s = State()
    s.schemas = []
    s.schemas.append('')
    assert s.schemas == []


def test_insert_empty():
    s = State()
    s.schemas = []
    s.schemas.insert(0, '')
    assert s.schemas == []
