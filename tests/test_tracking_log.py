# -*- coding: utf-8 -*-
import logging
from time import sleep

import pytest
from django.urls import reverse

from etools_datamart.api.endpoints import InterventionViewSet
from etools_datamart.apps.tracking.models import APIRequestLog

logger = logging.getLogger(__name__)


@pytest.yield_fixture
def user(admin_user):
    return admin_user


@pytest.yield_fixture
def django_app(django_app_mixin, user):
    APIRequestLog.objects.truncate()
    django_app_mixin._patch_settings()
    django_app_mixin.extra_environ = {'HTTP_X_SCHEMA': "bolivia,chad,lebanon",
                                      'REMOTE_ADDR': '192.168.66.66'
                                      }
    django_app_mixin.renew_app()
    django_app_mixin.app.set_user(user)
    yield django_app_mixin.app
    django_app_mixin._unpatch_settings()


@pytest.mark.django_db(transaction=True)
def test_log(enable_stats, django_app, admin_user):
    url = reverse("api:intervention-list")
    res = django_app.get(url)
    assert res.status_code == 200
    sleep(10)
    log = APIRequestLog.objects.get(path=url)

    assert log
    assert log.method == 'GET'
    assert log.content_type == 'application/json'
    assert log.remote_addr == '192.168.66.66'
    assert log.host == 'testserver'
    assert log.user == admin_user.username
    assert log.viewset == InterventionViewSet
    assert log.service == 'Intervention'
    assert not log.cached
