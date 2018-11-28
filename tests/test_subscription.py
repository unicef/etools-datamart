import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.subscriptions.views import subscribe


@pytest.fixture()
def etltask(db):
    EtlTask.objects.inspect()
    return EtlTask.objects.first()


@pytest.mark.django_db
def test_subscribe_create(rf, admin_user, etltask):
    request = rf.post(reverse("subscribe", args=[etltask.pk]),
                      {"type": 1}, content_type='application/json')
    request.user = admin_user
    res = subscribe(request, etltask.pk)

    data = json.loads(res.content)
    assert data["status"] == "created"


@pytest.mark.django_db
def test_subscribe_update(rf, admin_user, etltask):
    request = rf.post(reverse("subscribe", args=[etltask.pk]),
                      {"type": 1}, content_type='application/json')
    request.user = admin_user
    res = subscribe(request, etltask.pk)
    res = subscribe(request, etltask.pk)

    data = json.loads(res.content)
    assert data["status"] == "updated"


@pytest.mark.django_db
def test_subscribe_404(rf, admin_user, etltask):
    request = rf.post(reverse("subscribe", args=[etltask.pk]),
                      {"type": 1}, content_type='application/json')
    request.user = admin_user
    res = subscribe(request, 21)
    assert res.status_code == 404


@pytest.mark.django_db
def test_subscribe_invalid(rf, admin_user, etltask):
    request = rf.post(reverse("subscribe", args=[etltask.pk]),
                      {"type": 2}, content_type='application/json')
    request.user = admin_user
    res = subscribe(request, etltask.pk)
    assert res.status_code == 400


@pytest.mark.django_db
def test_subscribe_error(rf, etltask):
    request = rf.post(reverse("subscribe", args=[etltask.pk]),
                      {"type": 1}, content_type='application/json')
    request.user = AnonymousUser()
    res = subscribe(request, etltask.pk)
    assert res.status_code == 500
