# -*- coding: utf-8 -*-
from contextlib import contextmanager
from functools import partial

import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    assert client.login(username='admin', password='password')
    return client


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
