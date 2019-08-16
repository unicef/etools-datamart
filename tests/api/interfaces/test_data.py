# -*- coding: utf-8 -*-
import os
from functools import wraps

from django.urls import resolve

import pytest
from drf_api_checker.exceptions import StatusCodeError
from drf_api_checker.fs import get_filename
from drf_api_checker.pytest import contract
from drf_api_checker.recorder import BASE_DATADIR, Recorder
from drf_api_checker.utils import _write, load_response, serialize_response
from rest_framework.test import APIClient
from test_utilities.factories import factories_registry, UserFactory

from etools_datamart.api.urls import router


def clean_url2(method, url, data):
    return f"{method}_{url.strip('.').replace('/', '_')}_{str(data)}"


class MyRecorder(Recorder):
    @property
    def client(self):
        user = UserFactory(is_superuser=True)
        client = APIClient()
        client.force_authenticate(user)
        return client

    def get_response_filename(self, method, url, data):
        return get_filename(self.data_dir, clean_url2(method, url, data) + '.response.json')

    def _assertCALL(self, url, *, allow_empty=False, check_headers=True, check_status=True,
                    expect_errors=False, name=None, method='get', data=None):
        """
        check url for response changes

        :param url: url to check
        :param allow_empty: if True ignore empty response and 404 errors
        :param check_headers: check response headers
        :param check_status: check response status code
        :raises: ValueError
        :raises: AssertionError
        """
        self.view = resolve(url).func.cls
        m = getattr(self.client, method.lower())
        self.filename = self.get_response_filename(method, name or url, data)
        response = m(url, data=data)
        assert response.accepted_renderer
        payload = response.data
        if not allow_empty and not payload:
            raise ValueError(f"View {self.view} returned and empty json. Check your test")

        if response.status_code > 299 and not expect_errors:
            raise ValueError(f"View {self.view} unexpected response. {response.status_code} - {response.content}")

        if not allow_empty and response.status_code == 404:
            raise ValueError(f"View {self.view} returned 404 status code. Check your test")

        if not os.path.exists(self.filename) or os.environ.get('API_CHECKER_RESET', False):
            _write(self.filename, serialize_response(response))

        stored = load_response(self.filename)
        if (check_status) and response.status_code != stored.status_code:
            raise StatusCodeError(self.view, response.status_code, stored.status_code)
        if check_headers:
            self._assert_headers(response, stored)
        self.compare(payload, stored.data, self.filename, view=self.view)


def frozenfixture2(use_request=False):
    def deco(func):
        from drf_api_checker.utils import load_fixtures, dump_fixtures
        from drf_api_checker.fs import mktree

        @wraps(func)
        def _inner(*args, **kwargs):
            parts = [os.path.dirname(func.__code__.co_filename),
                     BASE_DATADIR,
                     func.__module__,
                     func.__name__, ]
            if 'request' in kwargs:
                request = kwargs['request']
                viewset = request.getfixturevalue('viewset')
                parts.append(viewset.__name__)

            destination = os.path.join(*parts
                                       ) + '.fixture.json'
            if os.path.exists(destination) and not os.environ.get('API_CHECKER_RESET'):
                return load_fixtures(destination)[func.__name__]
            mktree(os.path.dirname(destination))
            data = func(*args, **kwargs)
            dump_fixtures({func.__name__: data}, destination)
            return data

        return pytest.fixture(_inner)

    return deco


def pytest_generate_tests(metafunc, *args):
    if 'viewset' in metafunc.fixturenames:
        params = []
        ids = []
        for prefix, viewset, basenametry in router.registry:
            if prefix.startswith('datamart/'):
                sers = viewset.serializers_fieldsets.keys()
                for ser in sers:
                    params.append([viewset, ser])
                    ids.append(f'{viewset.__name__}-{ser}')
                # params.append(viewset)
                # ids.append(f'{viewset.__name__}')
        metafunc.parametrize("viewset,serializer", params, ids=ids)


@frozenfixture2()
def data(db, request):
    # TIPS: database access is forbidden in pytest_generate_tests
    viewset = request.getfixturevalue('viewset')
    factory = factories_registry[viewset.serializer_class.Meta.model]
    data = (factory(schema_name='bolivia'),
            factory(schema_name='chad'),
            factory(schema_name='lebanon'))
    return data


@contract(recorder_class=MyRecorder, headers=False)
def test_list(viewset, serializer, data):
    url = f"{viewset.get_service().endpoint}"
    return [url, {'-serializer': serializer}]


@frozenfixture2()
def record(db, request):
    # TIPS: database access is forbidden in pytest_generate_tests
    viewset = request.getfixturevalue('viewset')
    factory = factories_registry[viewset.serializer_class.Meta.model]
    return factory(schema_name='bolivia')


@contract(recorder_class=MyRecorder)
def test_record(viewset, serializer, record):
    url = f"{viewset.get_service().endpoint}{record.pk}/"
    return url
