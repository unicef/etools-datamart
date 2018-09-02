# -*- coding: utf-8 -*-
import pytest
from rest_framework.reverse import reverse

from etools_datamart.api.endpoints import PartnerViewSet
from etools_datamart.api.urls import router
from etools_datamart.apps.etools.models import PartnersPartnerorganization
from etools_datamart.apps.multitenant.postgresql.utils import current_schema
from etools_datamart.state import state

# def path_from_url(route):
#     return "/%s" % str(route.pattern).replace('^', '').replace('$', '')


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


def test_list_requires_schema(client):
    url = reverse("api:partners-list")
    res = client.get(url, HTTP_X_SCHEMA="")
    assert res.status_code == 400
    assert res.json()['error'] == "Please set X-Schema header with selected workspaces"


@pytest.mark.parametrize('schema', ['bolivia'])
@pytest.mark.parametrize('format', ['json', 'html', 'csv'])
def test_retrieve(client, url, format, schema):
    res = client.get(url, format=format, HTTP_X_SCHEMA=schema)
    assert state.schemas == [schema]
    assert res.status_code in [200, 404], res
    assert res.json()


def test_retrieve_requires_only_one_schema(client):
    url = reverse("api:partners-detail", args=['_lastest_'])
    res = client.get(url, HTTP_X_SCHEMA="bolivia,chad")
    assert res.status_code == 400
    assert res.json()['error'] == "Please set X-Schema header with only one workspace"


def test_retrieve_requires_one_schema(client):
    url = reverse("api:partners-detail", args=['_lastest_'])
    res = client.get(url, HTTP_X_SCHEMA="")
    assert res.status_code == 400
    assert res.json()['error'] == "Please set X-Schema header with selected workspace"


def test_retrieve_id(client):
    url = PartnerViewSet.get_service().endpoint
    with current_schema('bolivia'):
        target = PartnersPartnerorganization.objects.first()
    res = client.get(f"{url}{target.pk}/", HTTP_X_SCHEMA="bolivia")
    assert state.schemas == ["bolivia"]
    assert res.status_code == 200, res
    assert res.json()
