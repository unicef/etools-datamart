import collections
from contextlib import contextmanager
from functools import partial

import pytest
from drf_querystringfilter.filters import RexList
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
def _assert_duplicate_queries(config, connection=None, ignored=None):
    from django.test.utils import CaptureQueriesContext

    if connection is None:
        from django.db import connection

    ignored = RexList(ignored or [])
    verbose = config.getoption('verbose') > 0
    with CaptureQueriesContext(connection) as context:
        yield context
        queries = [q['sql'] for q in context.captured_queries]
        duplicates = [item for item, count in collections.Counter(queries).items()
                      if count > 1 and item not in ignored]
        if duplicates:
            msg = "Duplicated query detected"
            if verbose:
                msg += '\n\nQueries:\n========\n\n%s' % '\n\n'.join(duplicates)
            else:
                msg += " (add -v option to show queries)"
            pytest.fail(str(msg))


@pytest.fixture(scope='function')
def django_assert_no_duplicate_queries(pytestconfig, ignored=None):
    return partial(_assert_duplicate_queries, pytestconfig, ignored=ignored)


@pytest.fixture()
def anon_user(db):
    return AnonUserFactory()
