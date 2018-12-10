# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from test_utilities.factories import InterventionFactory, SystemFilterFactory, UserAccessControlFactory
from unicef_rest_framework.models import Service
from unicef_rest_framework.test_utils import user_allow_country


@pytest.fixture(autouse=True)
def setup_data(db):
    datas = [InterventionFactory(country_name='bolivia'),
             InterventionFactory(country_name='chad'),
             InterventionFactory(country_name='lebanon')]
    yield
    [d.delete() for d in datas]


def test_user_system_filter(client: APIClient, data_service: Service, user1: User,
                            django_assert_no_duplicate_queries, settings,
                            django_assert_num_queries):
    settings.CACHES = {'api': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

    client.force_authenticate(user1)
    data_service.invalidate_cache()
    SystemFilterFactory(service=data_service, user=user1, rules={'country_name': 'bolivia'})
    UserAccessControlFactory(service=data_service, user=user1)
    with user_allow_country(user1, "bolivia"):
        with django_assert_no_duplicate_queries():
            res = client.get(data_service.endpoint)
    assert res.status_code == 200
    results = res.json()['results']
    assert res['system-filters'] == "country_name=bolivia"
    assert res['cache-hit'] == "False"
    assert len(results) == 1
    assert [r['country_name'] for r in results] == ['bolivia']
