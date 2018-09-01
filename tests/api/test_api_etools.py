# -*- coding: utf-8 -*-
import pytest
from rest_framework.reverse import reverse

from etools_datamart.api.urls import router
from etools_datamart.state import state


def path_from_url(route):
    return "/%s" % str(route.pattern).replace('^', '').replace('$', '')


def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        if metafunc.function.__name__ == 'test_list':
            urls = filter(lambda url: 'etools/' in url,
                          [reverse("api:%s" % url.name) for url in router.urls if url.name.endswith('-list')])
        elif metafunc.function.__name__ == 'test_retrieve':
            urls = filter(lambda url: 'etools/' in url,
                          [reverse("api:%s" % url.name, args=['_lastest_']) for url in router.urls if
                           url.name.endswith('-detail')])
        metafunc.parametrize("url", list(urls))


@pytest.mark.parametrize('schema', [['bolivia'], ['bolivia', 'chad']], ids=["single", "multiple"])
@pytest.mark.parametrize('format', ['json', 'html', 'csv'])
def test_list(client, url, format, schema):
    res = client.get(url, format=format, HTTP_X_SCHEMA=",".join(schema))
    assert state.schemas == schema
    assert res.status_code == 200, res
    assert res.json()


@pytest.mark.parametrize('schema', ['bolivia'])
@pytest.mark.parametrize('format', ['json', 'html', 'csv'])
def test_retrieve(client, url, format, schema):
    res = client.get(url, format=format, HTTP_X_SCHEMA=schema)
    assert state.schemas == [schema]
    assert res.status_code in [200, 404], res
    assert res.json()


def test_retrieve_requires_only_one_Schema(client):
    url = reverse("api:partners-detail", args=['_lastest_'])
    res = client.get(url, HTTP_X_SCHEMA="bolivia,chad")
    assert res.status_code == 400
    assert res.json()

# @pytest.mark.parametrize('schema', [['bolivia'], ['bolivia', 'chad']])
# @pytest.mark.parametrize('format', ['json', 'html'])
# def test_options(client, url, format, schema):
#     res = client.options(url, format=format, HTTP_X_SCHEMA=",".join(schema))
#     assert state.schemas == schema
#     assert res.status_code == 200, res
#     assert res.json()
