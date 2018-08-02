# -*- coding: utf-8 -*-
import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


def pytest_generate_tests(metafunc):
    urls = []
    if 'url' in metafunc.fixturenames:
        # TODO: inspect router
        urls = [reverse('api:partners-list'),
                reverse('api:reportsresult-list'),
                ]
        metafunc.parametrize("url", urls)


@pytest.mark.parametrize('schema', ['bolivia', 'bolivia,chad'])
@pytest.mark.parametrize('format', ['json', 'html'])
def test_partners(client, url, format, schema):
    res = client.get(url, format=format, HTTP_X_SCHEMA=schema)
    assert res.json()
