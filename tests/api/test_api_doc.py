# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse


def test_swagger(django_app):
    res = django_app.get(reverse('api:schema-swagger-ui'))
    assert res.status_code == 200
