# -*- coding: utf-8 -*-
from django.core.cache import caches
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


def test_index_default(django_app, admin_user, monkeypatch):
    url = reverse("admin:index")
    monkeypatch.setattr('etools_datamart.config.admin.cache', caches['redis'])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    # repeat to test caching
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_index_old(django_app, admin_user):
    django_app.set_cookie("old_index_style", "1")
    url = reverse("admin:index")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
