# -*- coding: utf-8 -*-
import pytest

from etools_datamart.api.endpoints import PartnerViewSet


def test_cache(client, admin_user, django_assert_num_queries,
               django_assert_no_duplicate_queries, settings):
    settings.CACHES = {'api': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
    service = PartnerViewSet.get_service()
    url = f"{service.endpoint}?country_name=bolivia"
    client.force_authenticate(admin_user)

    with django_assert_no_duplicate_queries():
        res = client.get(url)
    assert res.status_code == 200, res.content
    assert res['cache-version'] == str(service.cache_version)
    assert res['cache-ttl'] == '1y'
    key = res['cache-key']
    etag = res['etag']

    with django_assert_no_duplicate_queries():
        res = client.get(url)
    assert res.status_code == 200, res.content
    assert res['cache-version'] == str(service.cache_version)
    assert res['cache-key'] == key
    assert res['cache-ttl'] == '1y'
    assert res['etag'] == etag
    assert res['cache-hit'] == str(True)


def test_etag(client, admin_user, data_service, django_assert_num_queries):
    url = f"{data_service.endpoint}?country_name=bolivia"
    client.force_authenticate(admin_user)

    res = client.get(url, HTTP_X_SCHEMA="bolivia", HTTP_IF_NONE_MATCH='Not Set')
    assert res.status_code == 200
    assert res['cache-version'] == str(data_service.cache_version)
    assert res['etag']

    etag = res['etag']
    res = client.get(url, HTTP_X_SCHEMA="bolivia", HTTP_IF_NONE_MATCH=etag)
    assert res.status_code == 304
    assert res['etag'] == etag


@pytest.mark.parametrize("fmt", ["pdf", "csv", "xlsx", "xhtml", "json", "ms-xml", "xml", "ms-json"])
def test_cache_renderers(fmt, client, admin_user, data_service, django_assert_num_queries):
    url = f"{data_service.endpoint}?country_name=bolivia&format={fmt}"
    client.force_authenticate(admin_user)

    res = client.get(url, HTTP_IF_NONE_MATCH='Not Set')
    assert res.status_code == 200
    assert res['cache-version'] == str(data_service.cache_version)
    assert res['etag']

    etag = res['etag']
    res = client.get(url, HTTP_X_SCHEMA="bolivia", HTTP_IF_NONE_MATCH=etag)
    assert res.status_code == 304
    assert res['etag'] == etag
