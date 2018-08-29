# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse

from etools_datamart.state import state
from test_utilities.factories import InterventionFactory


@pytest.fixture()
def url():
    return reverse("admin:etools_partnerspartnerorganization_changelist")


def test_header(django_app, admin_user, url):
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,lebanon"})
    assert res.status_code == 200
    assert state.schemas == ['bolivia', 'lebanon']


def test_cookie(django_app, admin_user, url):
    django_app.set_cookie('schemas', 'bolivia,lebanon')
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    assert state.schemas == ['bolivia', 'lebanon']


def test_query_param(django_app, admin_user, url):
    url = f"{url}?_schemas=bolivia,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    assert state.schemas == ['bolivia', 'lebanon']


def test_precendece_1(django_app, admin_user, url):
    # schema selectio order should be
    # 1. query_params
    # 2. request header
    # 3. cookie
    url = f"{url}?_schemas=bolivia"
    django_app.set_cookie('schemas', 'chad')
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "lebanon"})
    assert res.status_code == 200
    assert state.schemas == ['bolivia']


def test_precendece_2(django_app, admin_user, url):
    # schema selectio order should be
    # 1. query_params
    # 2. request header
    # 3. cookie
    django_app.set_cookie('schemas', 'chad')
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "lebanon"})
    assert res.status_code == 200
    assert state.schemas == ['lebanon']


def test_api_call_header(client, admin_user):
    client.login(username='admin', password='password')

    url = reverse("api:partners-list")
    res = client.get(url, HTTP_X_SCHEMA="bolivia,lebanon")
    assert res.status_code == 200
    assert state.schemas == ['bolivia', 'lebanon']


def test_api_call_queryparam(client, admin_user):
    client.login(username='admin', password='password')

    url = f'{reverse("api:partners-list")}?_schemas=bolivia,lebanon'
    res = client.get(url)
    assert res.status_code == 200
    assert state.schemas == ['bolivia', 'lebanon']
    assert res['X-Schema'] == 'bolivia,lebanon'


def test_api_call_queryparam_conflict(client, admin_user):
    # properly handle both schema and country_name param
    #
    InterventionFactory(country_name="bolivia")
    InterventionFactory(country_name="lebanon")
    client.login(username='admin', password='password')

    url = f'{reverse("api:intervention-list")}?_schemas=bolivia&country_name=lebanon'
    res = client.get(url)
    assert res.status_code == 200
    assert not list(filter(lambda x: x['country_name'] != 'lebanon', res.json()['results']))
    assert 'X-Schema' not in res


def test_queryparam_api_vs_admin(client, django_app, admin_user):
    # properly handle both schema and country_name param
    #
    InterventionFactory(country_name="bolivia")
    InterventionFactory(country_name="lebanon")
    client.login(username='admin', password='password')

    url = f'{reverse("api:intervention-list")}?_schemas=bolivia&country_name=lebanon'
    res = client.get(url)
    assert res.status_code == 200
    assert not list(filter(lambda x: x['country_name'] != 'lebanon', res.json()['results']))

    url = f'{reverse("admin:data_intervention_changelist")}?_schemas=bolivia&country_name=lebanon'
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
