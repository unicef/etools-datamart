# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from test_utilities.factories import InterventionFactory, SystemFilterFactory
from unicef_rest_framework.models import Service


@pytest.fixture(autouse=True)
def setup_data(db):
    InterventionFactory(country_name='a')
    InterventionFactory(country_name='b')
    InterventionFactory(country_name='b')


def test_user_system_filter(client: APIClient, data_service: Service, user1: User):
    client.force_authenticate(user1)
    SystemFilterFactory(service=data_service, user=user1,
                        rules={'country_name': 'a'})
    res = client.get(data_service.endpoint, HTTP_X_SCHEMA="public")
    results = res.json()['results']
    assert [r['country_name'] for r in results] == ['a']
    assert len(results) == 1
