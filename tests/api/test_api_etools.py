# -*- coding: utf-8 -*-
import pytest
from rest_framework.reverse import reverse

from etools_datamart.api.endpoints import PartnerViewSet
from etools_datamart.api.urls import router
from etools_datamart.apps.etools.models import PartnersPartnerorganization
from etools_datamart.apps.multitenant.postgresql.utils import current_schema


def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        if metafunc.function.__name__ == 'test_list':
            urls = filter(lambda url: 'etools/' in url,
                          [reverse("api:%s" % url.name, args=['latest'])
                           for url in router.urls if url.name.endswith('-list')])
        elif metafunc.function.__name__ == 'test_retrieve':
            urls = filter(lambda url: 'etools/' in url,
                          [reverse("api:%s" % url.name, args=['latest', '_lastest_']) for url in router.urls if
                           url.name.endswith('-detail')])
        metafunc.parametrize("url", list(urls))


@pytest.mark.parametrize('schema', [['bolivia'], ['bolivia', 'chad']], ids=["single", "multiple"])
@pytest.mark.parametrize('format', ['json', 'html', 'csv'])
def test_list(client, url, format, schema):
    url = f"{url}?country_name={','.join(schema)}"
    res = client.get(url, format=format)

    assert res.status_code == 200, res.content
    assert res.json()


def test_list_with_no_schema_search_all_schemas(client):
    url = reverse("api:partners-list", args=['latest'])
    res = client.get(url)
    assert res.status_code == 200, res.content


@pytest.mark.parametrize('format', ['json', 'html', 'csv'])
def test_retrieve(client, url, format):
    url = f"{url}?country_name=bolivia"
    res = client.get(url, format=format)
    assert res.status_code in [200, 404], res
    assert res.json()


def test_retrieve_requires_only_one_schema(client):
    url = reverse("api:partners-detail", args=['latest', '_lastest_'])
    url = f"{url}?country_name=bolivia,chad"
    res = client.get(url)
    assert res.status_code == 400, res.content
    assert res.json()['error'] == "only one country is allowed"


def test_retrieve_requires_one_schema(client):
    url = reverse("api:partners-detail", args=['latest', '_lastest_'])
    res = client.get(url)
    assert res.status_code == 400
    assert res.json()['error'] == "country_name parameter is mandatory"


def test_retrieve_id(client):
    url = PartnerViewSet.get_service().endpoint
    with current_schema('bolivia'):
        target = PartnersPartnerorganization.objects.first()
    res = client.get(f"{url}{target.pk}/?country_name=bolivia")
    assert res.status_code == 200, res
    assert res.json()
