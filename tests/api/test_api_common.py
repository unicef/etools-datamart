# -*- coding: utf-8 -*-
from unittest.mock import Mock

import pytest
from django.http import Http404
from drf_querystringfilter.exceptions import QueryFilterException
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.reverse import reverse

from etools_datamart.api.endpoints.common import APIReadOnlyModelViewSet
from etools_datamart.api.urls import router
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema


def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        urls = [reverse("api:%s" % url.name) for url in router.urls
                if url.name.endswith('-list')]
        metafunc.parametrize("url", urls, ids=urls)


def test_options(client, url):
    res = client.options(url)
    assert res.status_code == 200, res
    assert res.json()


@pytest.mark.parametrize("exc, code", [(QueryFilterException, 400),
                                       (NotAuthenticated, 401),
                                       (Http404, 404),
                                       (NotAuthorizedSchema, 403),
                                       (PermissionDenied, 403),
                                       (InvalidSchema, 400),
                                       (AuthenticationFailed, 403),
                                       ])
def test_handle_exception(client, exc, code):
    view = APIReadOnlyModelViewSet()
    view.request = Mock()
    res = view.handle_exception(exc(""))
    assert res.status_code == code
