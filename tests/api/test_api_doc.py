# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse


def test_swagger_json(django_app, db):
    res = django_app.get(reverse('api:schema-json', args=['.json']))
    assert res.status_code == 200


def test_swagger(django_app, db):
    res = django_app.get(reverse('api:schema-swagger-ui'))
    assert res.status_code == 200


def test_swagger_openapi(django_app, db):
    res = django_app.get("%s?format=openapi" % reverse('api:schema-swagger-ui'))
    assert res.status_code == 200


def test_core_api(django_app, db):
    res = django_app.get(reverse('api:schema-redoc'))
    assert res.status_code == 200
