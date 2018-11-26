# -*- coding: utf-8 -*-
import pytest
from django.contrib import messages
from django.urls import reverse
from test_utilities.factories import PMPIndicatorFactory
from test_utilities.perms import user_grant_permissions


@pytest.mark.django_db()
def test_data_index(django_app, admin_user):
    url = reverse("admin:app_list", args=['data'])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db()
def test_pmpindicators_list(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db()
def test_pmpindicators_filter(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    url = f"{url}?country_name=bolivia,chad,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db()
def test_pmpindicators_detail(django_app, staff_user, settings):
    i = PMPIndicatorFactory()
    url = reverse("admin:data_pmpindicators_change", args=[i.pk])
    assert staff_user.is_authenticated
    with user_grant_permissions(staff_user, ['data.change_pmpindicators']):
        res = django_app.get(url, user=staff_user)
        assert res.status_code == 200
        res = res.form.submit().follow()
        assert res.status_code == 200
        storage = res.context['messages']
        assert [m.message for m in storage] == ['This admin is read-only. Record not saved.']


@pytest.mark.django_db()
def test_pmpindicators_detail_supersuser(django_app, admin_user, settings):
    i = PMPIndicatorFactory()
    url = reverse("admin:data_pmpindicators_change", args=[i.pk])
    assert admin_user.is_authenticated
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.form.submit().follow()
    assert res.status_code == 302


def test_pmpindicators_refresh(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Refresh").follow()
    assert res.status_code == 200
    storage = res.context['messages']
    assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]


def test_pmpindicators_invalidate_cache(django_app, admin_user, service):
    url = reverse("admin:data_pmpindicators_invalidate_cache")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 302


def test_pmpindicators_api(django_app, admin_user, service):
    url = reverse("admin:data_pmpindicators_api")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 302


def test_pmpindicators_truncate(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Truncate")
    assert res.status_code == 200
    res = res.form.submit().follow()
    assert res.status_code == 200
    storage = res.context['messages']
    assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]


def test_pmpindicators_queue(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Queue").follow()
    assert res.status_code == 200
    storage = res.context['messages']
    assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]


def test_pmpindicators_filterimng(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(f"{url}", user=admin_user)
    assert res.status_code == 200
