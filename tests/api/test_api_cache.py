# -*- coding: utf-8 -*-
import logging

import pytest
from unicef_rest_framework.models import Service

from etools_datamart.api.endpoints import InterventionViewSet

logger = logging.getLogger(__name__)


@pytest.fixture()
def service(db):
    service, __ = Service.objects.get_for_viewset(InterventionViewSet)
    service.invalidate_cache()
    return service


def test_cache(client, admin_user, service, django_assert_num_queries,
               django_assert_no_duplicate_queries, settings):
    settings.CACHES = {'api': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
    # settings.CACHES = {'api': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

    url = service.endpoint
    client.force_authenticate(admin_user)

    with django_assert_no_duplicate_queries():
        # with django_assert_num_queries(5):
        res = client.get(url, HTTP_X_SCHEMA="bolivia")
    assert res.status_code == 200
    assert res['cache-version'] == str(service.cache_version)
    assert res['cache-ttl'] == '1y'
    key = res['cache-key']
    etag = res['etag']

    with django_assert_no_duplicate_queries():
        res = client.get(url, HTTP_X_SCHEMA="bolivia")
    assert res.status_code == 200
    assert res['cache-version'] == str(service.cache_version)
    assert res['cache-key'] == key
    assert res['cache-ttl'] == '1y'
    assert res['etag'] == etag
    assert res['cache-hit'] == str(True)


def test_etag(client, admin_user, service, django_assert_num_queries):
    url = service.endpoint
    client.force_authenticate(admin_user)

    res = client.get(url, HTTP_X_SCHEMA="bolivia", HTTP_IF_NONE_MATCH='Not Set')
    assert res.status_code == 200
    assert res['cache-version'] == str(service.cache_version)
    assert res['etag']

    etag = res['etag']
    res = client.get(url, HTTP_X_SCHEMA="bolivia", HTTP_IF_NONE_MATCH=etag)
    assert res.status_code == 304
    assert res['etag'] == etag
