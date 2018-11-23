# -*- coding: utf-8 -*-
from django.urls import reverse


def test_home(django_app, admin_user):
    res = django_app.get(reverse('home'))
    assert res.status_code == 200


def test_monitor(django_app, admin_user):
    res = django_app.get(reverse('monitor'))
    assert res.status_code == 200
