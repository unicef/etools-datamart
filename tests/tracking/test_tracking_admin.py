from django.urls import reverse


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
