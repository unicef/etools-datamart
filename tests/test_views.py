# -*- coding: utf-8 -*-


def test_home(django_app, admin_user):
    res = django_app.get('/')
    assert res.status_code == 200
