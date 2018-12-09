# -*- coding: utf-8 -*-
from contextlib import contextmanager
from functools import partial

import pytest
from rest_framework.test import APIClient
from test_utilities.factories import AnonUserFactory
from unicef_rest_framework.models import Service

from etools_datamart.api.endpoints import InterventionViewSet


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    assert client.login(username='admin', password='password')
    return client


@pytest.fixture()
def service(db):
    Service.objects.load_services()
    return Service.objects.order_by('?').first()


@pytest.fixture()
def etools_service(db):
    Service.objects.load_services()
    return Service.objects.get(viewset=InterventionViewSet)


@pytest.fixture()
def data_service(db):
    Service.objects.load_services()
    return Service.objects.get(viewset=InterventionViewSet)


@contextmanager
def _assert_duplicate_queries(config, connection=None):
    from django.test.utils import CaptureQueriesContext

    if connection is None:
        from django.db import connection

    verbose = config.getoption('verbose') > 0
    with CaptureQueriesContext(connection) as context:
        yield context
        unique = {q['sql'] for q in context.captured_queries}
        if len(unique) != len(context.captured_queries):
            msg = "Duplicated query detected"
            if verbose:
                sqls = (q['sql'] for q in context.captured_queries)
                msg += '\n\nQueries:\n========\n\n%s' % '\n\n'.join(sqls)
            else:
                msg += " (add -v option to show queries)"
            pytest.fail(msg)


@pytest.fixture(scope='function')
def django_assert_no_duplicate_queries(pytestconfig):
    return partial(_assert_duplicate_queries, pytestconfig)


@pytest.fixture()
def anon_user(db):
    return AnonUserFactory()
