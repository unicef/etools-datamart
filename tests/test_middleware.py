# -*- coding: utf-8 -*-
import logging

import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.urls import reverse

from etools_datamart.apps.multitenant.middleware import MultiTenantMiddleware

# from etools_datamart.state import State

logger = logging.getLogger(__name__)


class State(list):
    valid = None


@pytest.fixture()
def middleware(db):
    return MultiTenantMiddleware(lambda request: HttpResponse())


@pytest.fixture()
def state(db, monkeypatch):
    state = State()
    monkeypatch.setattr('etools_datamart.apps.multitenant.middleware.state', state)


def test_valid(middleware, rf, state):
    request = rf.get("/", HTTP_X_SCHEMA="bolivia")
    assert middleware(request)


def test_invalid(middleware, rf, state):
    request = rf.get("/")
    assert middleware(request)


def test_no_schema_anonymous(middleware, rf, state):
    request = rf.get("/admin/")
    request.user = AnonymousUser()
    assert middleware(request)


def test_no_schema_logged(middleware, rf, state, admin_user):
    request = rf.get("/admin/")
    request.user = admin_user
    response = middleware(request)
    assert response.status_code == 302


def test_no_schema_selection_url(middleware, rf, state, admin_user):
    select_schema_url = reverse('select-schema')
    request = rf.get(select_schema_url)
    request.user = admin_user
    response = middleware(request)
    assert response.status_code == 200
