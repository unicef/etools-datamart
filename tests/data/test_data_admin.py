# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse
from test_utilities.factories import PMPIndicatorFactory


@pytest.mark.django_db()
def test_pmpindicators_list(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200


@pytest.mark.django_db()
def test_pmpindicators_detail(django_app, admin_user, settings):
    i = PMPIndicatorFactory()
    url = reverse("admin:data_pmpindicators_change", args=[i.pk])
    assert admin_user.is_authenticated
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200
    res = res.form.submit()
    assert res.status_code == 302


@pytest.mark.django_db()
def test_pmpindicators_refresh(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_refresh")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 302


@pytest.mark.django_db()
def test_pmpindicators_queue(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_queue")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 302


@pytest.mark.django_db()
def test_pmpindicators_truncate(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_truncate")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200
