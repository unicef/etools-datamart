from django.urls import reverse

import pytest

from etools_datamart.apps.etl.models import EtlTask


def test_home(django_app, admin_user):
    res = django_app.get(reverse("home"))
    assert res.status_code == 200


def test_login(django_app, admin_user):
    res = django_app.get(reverse("login"))
    assert res.status_code == 200


@pytest.mark.django_db
def test_whoami(django_app, admin_user):
    res = django_app.get(reverse("whoami"), user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db
def test_whoami_anon(django_app):
    res = django_app.get(reverse("whoami"))
    assert res.status_code == 200


def test_monitor(django_app, admin_user):
    EtlTask.objects.inspect()
    res = django_app.get(reverse("monitor"), user=admin_user)
    assert res.status_code == 200


def test_profile(django_app, admin_user):
    res = django_app.get(reverse("profile"), user=admin_user)
    assert res.status_code == 200


def test_profile_post(django_app, user):
    res = django_app.get(reverse("profile"), user=user)
    res = res.form.submit()
    assert res.status_code == 200
