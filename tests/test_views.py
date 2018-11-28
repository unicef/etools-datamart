# -*- coding: utf-8 -*-
from django.urls import reverse

from etools_datamart.apps.etl.models import EtlTask


def test_home(django_app, admin_user):
    res = django_app.get(reverse('home'))
    assert res.status_code == 200


def test_monitor(django_app, admin_user):
    EtlTask.objects.inspect()
    res = django_app.get(reverse('monitor'), user=admin_user)
    assert res.status_code == 200
