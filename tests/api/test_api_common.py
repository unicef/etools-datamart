# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse

from etools_datamart.api.urls import router

# def path_from_url(route):
#     return "/%s" % str(route.pattern).replace('^', '').replace('$', '')


def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        urls = [reverse("api:%s" % url.name) for url in router.urls if url.name.endswith('-list')]
        metafunc.parametrize("url", urls)


def test_options(client, url):
    res = client.options(url, HTTP_X_SCHEMA="public")
    assert res.status_code == 200, res
    assert res.json()
