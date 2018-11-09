from django.urls import reverse

from etools_datamart.apps.tracking.utils import refresh_all_counters


def test_changelist(django_app, admin_user, log):
    url = reverse("admin:tracking_apirequestlog_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_changelist2(django_app, admin_user, log_with_params):
    url = reverse("admin:tracking_apirequestlog_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_change(django_app, admin_user, log):
    url = reverse("admin:tracking_apirequestlog_change", args=[log.pk])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_aggregate(django_app, admin_user, log):
    url = reverse("admin:tracking_apirequestlog_changelist")
    res = django_app.get(url, user=admin_user)
    res.click("Aggregate")
    assert res.status_code == 200


def test_tracking_index(django_app, admin_user):
    url = reverse("admin:app_list", args=['tracking'])
    refresh_all_counters()
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_tracking_reset(django_app, admin_user):
    url = reverse("admin:tracking-reset")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 302


def test_tracking_refresh(django_app, admin_user):
    url = reverse("admin:tracking-refresh")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 302
