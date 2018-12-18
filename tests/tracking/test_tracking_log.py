# -*- coding: utf-8 -*-
import logging

import pytest
# from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from etools_datamart.api.endpoints import InterventionViewSet
# from etools_datamart.apps.tracking.middleware import StatsMiddleware, ThreadedStatsMiddleware
from etools_datamart.apps.tracking.models import APIRequestLog, DailyCounter

# from time import sleep
# from unittest.mock import Mock

# from test_utilities.factories import AdminFactory, UserFactory


logger = logging.getLogger(__name__)


@pytest.fixture
def user(admin_user):
    return admin_user


@pytest.fixture
def django_app(django_app_mixin, system_user):
    APIRequestLog.objects.truncate()
    django_app_mixin._patch_settings()
    django_app_mixin.extra_environ = {'REMOTE_ADDR': '192.168.66.66'}
    django_app_mixin.renew_app()
    django_app_mixin.app.set_user(system_user)
    yield django_app_mixin.app
    django_app_mixin._unpatch_settings()


@pytest.mark.django_db
def test_log(enable_stats, django_app, system_user, reset_stats):
    url = reverse("api:intervention-list", args=['v1'])
    url = f"{url}?country_name=bolivia,chad,lebanon"

    res = django_app.get(url)
    assert res.status_code == 200
    log = APIRequestLog.objects.first()
    assert log
    assert log.method == 'GET'
    assert log.content_type == 'application/json'
    assert log.remote_addr == '192.168.66.66'
    assert log.host == 'testserver'
    assert log.user == system_user
    assert log.viewset == InterventionViewSet
    assert log.service == 'Intervention'
    assert not log.cached

    daily = DailyCounter.objects.get(day=log.requested_at)
    assert daily.total == 1
    assert daily.response_max == log.response_ms
    assert daily.response_min == log.response_ms
    assert daily.response_average == log.response_ms


# @pytest.mark.django_db
# def test_threaedlog(enable_threadstats, django_app, admin_user):
#     url = reverse("api:intervention-list", args=['v1'])
#     url = f"{url}?country_name=bolivia,chad,lebanon"
#
#     res = django_app.get(url)
#     assert res.status_code == 200


# @pytest.mark.parametrize("code", [200, 500])
# @pytest.mark.parametrize("stats", [True, False])
# @pytest.mark.parametrize("user_type", [AnonymousUser, UserFactory, AdminFactory])
# @pytest.mark.parametrize("middleware", [StatsMiddleware, ThreadedStatsMiddleware])
# @pytest.mark.django_db(transaction=True)
# def test_middleware(rf, settings, user_type, middleware, stats, code):
#     user = user_type()
#     settings.ENABLE_LIVE_STATS = stats
#
#     view = InterventionViewSet.as_view({'get': 'list'})
#     service = InterventionViewSet.get_service()
#     url = service.endpoint
#
#     m = middleware(lambda r: Mock(status_code=code, content='abc',
#                                   accepted_media_type='text/plain'))
#     request = rf.get(url)
#     request.user = user
#     request.api_info = {'view': view,
#                         'service': service}
#     m(request)
#     m(request)  # two times to trigger ENABLE_LIVE_STATS
#     sleep(1)
#     log = APIRequestLog.objects.filter(path=url).first()
#     if code == 200:
#         assert log
#     else:
#         assert not log
#
