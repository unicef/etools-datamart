# -*- coding: utf-8 -*-
from django.db import connections
from django.urls import reverse

conn = connections['etools']


def test_constance(django_app, admin_user):
    url = reverse("admin:constance_config_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_sysinfo(django_app, admin_user):
    url = reverse("sys-admin-info")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_index(django_app, admin_user):
    url = reverse("admin:index")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
