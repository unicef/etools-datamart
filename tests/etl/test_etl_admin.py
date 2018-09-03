# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse
from test_utilities.factories import TaskLogFactory


@pytest.fixture
def tasklog():
    return TaskLogFactory()


def test_tasklog_changelist(django_app, admin_user, tasklog):
    url = reverse("admin:etl_tasklog_changelist")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200


def test_tasklog_change(django_app, admin_user, tasklog):
    url = reverse("admin:etl_tasklog_change", args=[tasklog.id])
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200


def test_tasklog_refresh(django_app, admin_user, tasklog):
    url = reverse("admin:etl_tasklog_change", args=[tasklog.id])
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200


def test_tasklog_truncate(django_app, admin_user, tasklog):
    url = reverse("admin:etl_tasklog_changelist")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200
    res = res.click("Truncate")
    assert res.status_code == 200
    res = res.form.submit()
    assert res.status_code == 302


def test_tasklog_inspect(django_app, admin_user, tasklog):
    url = reverse("admin:etl_tasklog_changelist")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "public"})
    assert res.status_code == 200
    res = res.click("Inspect")
    assert res.status_code == 302
