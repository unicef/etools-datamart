# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from test_utilities.factories import InterventionFactory, SystemFilterFactory, UserAccessControlFactory
from unicef_rest_framework.models import Service


@pytest.fixture(autouse=True)
def setup_data(db):
    datas = [InterventionFactory(country_name='a'),
             InterventionFactory(country_name='b'),
             InterventionFactory(country_name='b')]
    yield
    [d.delete() for d in datas]


def test_user_system_filter(client: APIClient, data_service: Service, user1: User,
                            django_assert_no_duplicate_queries, settings):
    settings.CACHES = {'api': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

    client.force_authenticate(user1)
    data_service.invalidate_cache()
    SystemFilterFactory(service=data_service, user=user1,
                        rules={'country_name': 'a'})
    UserAccessControlFactory(service=data_service, user=user1)
    with django_assert_no_duplicate_queries():
        # with django_assert_num_queries(7):
        res = client.get(data_service.endpoint, HTTP_X_SCHEMA="public")
    assert res.status_code == 200
    results = res.json()['results']
    assert res['system-filters'] == "country_name=a"
    assert res['cache-hit'] == "False"
    assert len(results) == 1
    assert [r['country_name'] for r in results] == ['a']
