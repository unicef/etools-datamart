import base64
import json
from unittest.mock import MagicMock

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.urls import reverse

import pytest
from test_utilities.factories import EmailTemplateFactory, HACTFactory, SubscriptionFactory

from unicef_rest_framework.test_utils import user_allow_service

from etools_datamart.apps.data.models import HACT
from etools_datamart.apps.etl.models import EtlTask
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


@pytest.mark.django_db
def test_notification_email(subscription: Subscription, email_templates):
    with user_allow_service(subscription.user, subscription.viewset):
        emails = Subscription.objects.notify(subscription.content_type.model_class())
    assert len(emails) == 1
    assert emails[0].to == [subscription.user.email]
    assert emails[0].attachments.count() == 0


@pytest.mark.django_db
def test_notification_email_attachment(subscription_attachment: Subscription, email_templates):
    with user_allow_service(subscription_attachment.user, subscription_attachment.viewset):
        emails = Subscription.objects.notify(subscription_attachment.content_type.model_class())
    assert len(emails) == 1
    assert emails[0].to == [subscription_attachment.user.email]
    assert emails[0].attachments.count() == 1


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
