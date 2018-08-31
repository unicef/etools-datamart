# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from test_utilities.factories import InterventionFactory, SystemFilterFactory
from unicef_rest_framework.models import Service


@pytest.fixture(autouse=True)
def setup_data(db):
    datas = [InterventionFactory(country_name='a'),
             InterventionFactory(country_name='b'),
             InterventionFactory(country_name='b')]
    yield
    [d.delete() for d in datas]


def setup_module(module):
    """ setup any state specific to the execution of the given module."""


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """


def test_user_system_filter(client: APIClient, data_service: Service, user1: User):
    client.force_authenticate(user1)
    SystemFilterFactory(service=data_service, user=user1,
                        rules={'country_name': 'a'})
    res = client.get(data_service.endpoint, HTTP_X_SCHEMA="public")
    results = res.json()['results']
    assert [r['country_name'] for r in results] == ['a']
    assert len(results) == 1
