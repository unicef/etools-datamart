import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from test_utilities.factories import EmailTemplateFactory, SubscriptionFactory
from unicef_rest_framework.test_utils import user_allow_service

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.subscriptions.models import Subscription
from etools_datamart.apps.subscriptions.views import subscribe


@pytest.fixture()
def etltask(db):
    EtlTask.objects.inspect()
    return EtlTask.objects.first()


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
    res = subscribe(request, 21)
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
