import base64
import json
from unittest.mock import MagicMock

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.urls import reverse

import pytest
from test_utilities.factories import EmailTemplateFactory, HACTFactory, SubscriptionFactory

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.mart.data.models import HACT
from etools_datamart.apps.subscriptions.models import Subscription
from etools_datamart.apps.subscriptions.urls import http_basic_auth
from etools_datamart.apps.subscriptions.views import subscribe


@pytest.fixture()
def etltask(db):
    HACTFactory()
    EtlTask.objects.inspect()
    return EtlTask.objects.get_for_model(HACT)


@pytest.fixture()
def subscription(etltask):
    return SubscriptionFactory(content_type=etltask.content_type,
                               type=Subscription.MESSAGE)


@pytest.fixture()
def subscription_attachment(etltask):
    return SubscriptionFactory(content_type=etltask.content_type,
                               type=Subscription.EXCEL)


@pytest.fixture()
def email_templates():
    return (EmailTemplateFactory(name='dataset_changed'),
            EmailTemplateFactory(name='dataset_changed_attachment'))


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
    res = subscribe(request, -99)
    assert res.status_code == 404


@pytest.mark.django_db
def test_subscribe_invalid(rf, admin_user, etltask):
    request = rf.post(reverse("subscribe", args=[etltask.pk]),
                      {"type": 99}, content_type='application/json')
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


def test_http_basic_auth_401(rf):
    request = rf.get('/')
    request.user = AnonymousUser()

    def view(request):
        return 11

    f = http_basic_auth(view)
    res = f(request)
    assert res.status_code == 401


def test_http_basic_auth_401b(rf, admin_user):
    string = '%s:%s' % ('admin', '--')
    base64string = base64.standard_b64encode(string.encode('utf-8'))
    request = rf.get('/', HTTP_AUTHORIZATION="Digest %s" % base64string.decode('utf-8'))
    request.user = AnonymousUser()
    request.session = MagicMock()

    def view(request):
        return HttpResponse("Ok")

    f = http_basic_auth(view)
    res = f(request)
    assert res.status_code == 401


def test_http_basic_auth_400(rf, admin_user):
    string = '%s:%s' % ('admin', '--')
    base64string = base64.standard_b64encode(string.encode('utf-8'))
    request = rf.get('/', HTTP_AUTHORIZATION="Basic %s" % base64string.decode('utf-8'))
    request.user = AnonymousUser()
    request.session = MagicMock()

    def view(request):
        return HttpResponse("Ok")

    f = http_basic_auth(view)
    res = f(request)
    assert res.status_code == 403


def test_http_basic_auth_200(rf, admin_user):
    string = '%s:%s' % ('admin', 'password')
    base64string = base64.standard_b64encode(string.encode('utf-8'))
    request = rf.get('/', HTTP_AUTHORIZATION="Basic %s" % base64string.decode('utf-8'))
    request.user = AnonymousUser()
    request.session = MagicMock()

    def view(request):
        return HttpResponse("Ok")

    f = http_basic_auth(view)
    res = f(request)
    assert res.status_code == 200
