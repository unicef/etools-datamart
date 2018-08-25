# -*- coding: utf-8 -*-
import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from etools_datamart.api.urls import router
from etools_datamart.state import state


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    assert client.login(username='admin', password='password')
    return client


def path_from_url(route):
    return "/%s" % str(route.pattern).replace('^', '').replace('$', '')


def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        urls = filter(lambda url:'datamart' in url,
                      [reverse("api:%s" % url.name) for url in router.urls if url.name.endswith('-list')])
        metafunc.parametrize("url", urls)


@pytest.mark.parametrize('format', ['json', 'html'])
def test_partners(client, url, format):
    res = client.get(url, format=format, HTTP_X_SCHEMA="public")
    assert res.status_code == 200, res
    assert res.json()

#
# def test_options(client, url):
#     res = client.options(url, HTTP_X_SCHEMA="public")
#     assert res.status_code == 200, res
#     assert res.json()
