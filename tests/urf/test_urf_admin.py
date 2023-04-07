from django.urls import reverse


def test_service_changelist(django_app, admin_user, service):
    url = reverse("admin:unicef_rest_framework_service_changelist")
    res = django_app.get(url, user=admin_user, extra_environ={"HTTP_X_SCHEMA": "public"})
    assert res.status_code == 200


def test_service_change(django_app, admin_user, service):
    url = reverse("admin:unicef_rest_framework_service_change", args=[service.id])
    res = django_app.get(url, user=admin_user, extra_environ={"HTTP_X_SCHEMA": "public"})
    assert res.status_code == 200


def test_service_refresh(django_app, admin_user, service):
    url = reverse("admin:unicef_rest_framework_service_change", args=[service.id])
    res = django_app.get(url, user=admin_user, extra_environ={"HTTP_X_SCHEMA": "public"})
    assert res.status_code == 200
