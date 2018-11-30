# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse
from test_utilities.factories import InterventionFactory


@pytest.mark.django_db()
def test_api_site_root(django_app, admin_user):
    url = reverse("api:api-root", args=['latest'])
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon",
                                        'HTTP_ACCEPT': 'text/html'})
    assert res.status_code == 200


@pytest.mark.django_db()
def test_api_list(django_app, admin_user):
    url = reverse("api:intervention-list", args=['latest'])
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon",
                                        'HTTP_ACCEPT': 'text/html'})
    assert res.status_code == 200


@pytest.mark.django_db()
def test_api_detail(django_app, admin_user):
    i = InterventionFactory()
    url = reverse("api:intervention-detail", args=['latest', i.pk])
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon",
                                        'HTTP_ACCEPT': 'text/html'})
    assert res.status_code == 200
