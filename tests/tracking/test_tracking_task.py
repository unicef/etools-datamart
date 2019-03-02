# -*- coding: utf-8 -*-
from datetime import timedelta

from django.utils import timezone

import pytest
from test_utilities.factories import APIRequestLogFactory

from etools_datamart.apps.tracking.middleware import log_request
from etools_datamart.apps.tracking.models import APIRequestLog, DailyCounter, MonthlyCounter, PathCounter, UserCounter


@pytest.fixture
def data(db):
    APIRequestLog.objects.truncate()
    today = timezone.now()
    previous_date = today - timedelta(days=140)
    [APIRequestLogFactory(user=None, viewset=None, service=None, requested_at=previous_date)
     for i in range(30)]


def test_stream_aggregation(reset_stats, admin_user, settings):
    settings.ENABLE_LIVE_STATS = True
    today = timezone.now()
    lastMonth = today.replace(day=1)
    data = dict(requested_at=today,
                user=admin_user,
                path='/a/b/',
                remote_addr='192.168.10.10',
                response_ms=2000,
                cached=False,
                )
    log_request(**data)

    assert APIRequestLog.objects.get(requested_at=data['requested_at'])
    assert PathCounter.objects.get(day=data['requested_at'], path=data['path'])
    assert UserCounter.objects.get(day=data['requested_at'], user=data['user'])
    assert MonthlyCounter.objects.get(day=lastMonth)
    assert DailyCounter.objects.get(day=data['requested_at'], cached=0)
    dc = DailyCounter.objects.get(day=data['requested_at'], cached=0)
    assert str(dc)
    assert UserCounter.objects.count() == 1

    data['cached'] = True
    log_request(**data)

    assert APIRequestLog.objects.filter(requested_at=data['requested_at']).count() == 2
    assert UserCounter.objects.count() == 1

    assert PathCounter.objects.get(day=data['requested_at'], path=data['path'])
    assert UserCounter.objects.get(day=data['requested_at'], user=data['user'])
    assert MonthlyCounter.objects.get(day=lastMonth, user=data['user'])

    d = DailyCounter.objects.get(day=data['requested_at'])
    assert d.total == 2
    assert d.cached == 1
    assert d.users == 1
