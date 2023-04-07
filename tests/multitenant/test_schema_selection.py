from django.db import connections
from django.urls import reverse

import pytest

from etools_datamart.apps.multitenant.exceptions import InvalidSchema

conn = connections["etools"]


@pytest.fixture()
def url():
    return reverse("admin:etools_partnerspartnerorganization_changelist")


# def test_cookie(django_app, admin_user, url):
#     django_app.set_cookie('schemas', 'bolivia,lebanon')
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     assert conn.schemas == ['bolivia', 'lebanon']


def test_wrong_schema(django_app, admin_user, url):
    url = f"{url}?country_name=xxx"
    with pytest.raises(InvalidSchema):
        django_app.get(url, user=admin_user)


def test_query_param(django_app, admin_user, url):
    url = f"{url}?country_name=bolivia,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    assert conn.schemas == ["bolivia", "lebanon"]


def test_select_schema_tenant(django_app, admin_user):
    _from = reverse("admin:etools_partnerspartnerorganization_changelist")
    url = f"{reverse('select-schema')}?from={_from}"
    res = django_app.get(url, user=admin_user)
    res.form["bolivia"] = True
    res = res.form.submit().follow()
    assert res.status_code == 200
    qs = res.context["cl"].queryset
    assert {e.schema for e in qs.all()} == {"bolivia"}
    assert conn.schemas == [
        "bolivia",
    ]


def test_select_schema_all_tenant(django_app, admin_user):
    _from = reverse("admin:etools_partnerspartnerorganization_changelist")
    url = f"{reverse('select-schema')}?from={_from}"
    res = django_app.get(url, user=admin_user)
    res.form["bolivia"] = True
    res.form["lebanon"] = True
    res.form["chad"] = True
    res = res.form.submit()
    assert res["Location"] == _from
    res = res.follow()
    assert res.status_code == 200


def test_select_schema_data(django_app, admin_user):
    _from = reverse("admin:data_intervention_changelist")
    url = f"{reverse('select-schema')}?from={_from}"
    res = django_app.get(url, user=admin_user)
    res.form["bolivia"] = True
    res = res.form.submit().follow()
    assert res.status_code == 200


#
# def test_precendece_2(django_app, admin_user, url):
#     # schema selectio order should be
#     # 1. query_params
#     # 3. cookie
#     django_app.set_cookie('schemas', 'chad')
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     assert conn.schemas == ['lebanon']

#
# def test_api_call_queryparam(client, admin_user):
#     client.login(username='admin', password='password')
#
#     url = f'{reverse("api:partner-list", args=["v1"])}?country_name=bolivia,lebanon'
#     res = client.get(url)
#     assert res.status_code == 200
#     assert conn.schemas == ['bolivia', 'lebanon']
#     # assert res['X-Schema'] == 'bolivia,lebanon'

# def test_api_call_queryparam_conflict(client, admin_user):
#     # properly handle both schema and country_name param
#     #
#     InterventionFactory(country_name="bolivia")
#     InterventionFactory(country_name="lebanon")
#     client.login(username='admin', password='password')
#
#     url = f'{reverse("api:intervention-list")}?country_name=bolivia&country_name=lebanon'
#     res = client.get(url)
#     assert res.status_code == 200
#     assert not list(filter(lambda x: x['country_name'] != 'lebanon', res.json()['results']))
#     assert 'X-Schema' not in res


# def test_queryparam_api_vs_admin(client, django_app, admin_user):
#     # properly handle both schema and country_name param
#     #
#     InterventionFactory(country_name="bolivia")
#     InterventionFactory(country_name="lebanon")
#     client.login(username='admin', password='password')
#
#     url = f'{reverse("api:intervention-list")}?country_name=bolivia&country_name=lebanon'
#     res = client.get(url)
#     assert res.status_code == 200
#     assert not list(filter(lambda x: x['country_name'] != 'lebanon', res.json()['results']))
#
#     url = f'{reverse("admin:data_intervention_changelist")}?country_name=bolivia&country_name=lebanon'
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
