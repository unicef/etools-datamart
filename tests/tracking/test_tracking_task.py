# -*- coding: utf-8 -*-

from datetime import timedelta

import pytest
from django.utils import timezone
from test_utilities.factories import APIRequestLogFactory, UserFactory

from etools_datamart.apps.tracking.models import APIRequestLog, DailyCounter
from etools_datamart.apps.tracking.tasks import task_aggregate_log


@pytest.fixture
def data(db):
    APIRequestLog.objects.truncate()
    today = timezone.now()
    previous_date = today - timedelta(days=140)
    [APIRequestLogFactory(user=None, viewset=None, service=None, requested_at=previous_date)
     for i in range(30)]


def test_aggregate_logs(db):
    APIRequestLog.objects.truncate()

    today = timezone.now().date()
    previous_date = today - timedelta(days=140)
    recent_date = today - timedelta(days=10)

    user1 = UserFactory()
    user2 = UserFactory()
    APIRequestLogFactory(user=user1, viewset=None, service=None, requested_at=previous_date)
    APIRequestLogFactory(user=user2, viewset=None, service=None, requested_at=previous_date)

    APIRequestLog.objects.aggregate()

    assert APIRequestLog.objects.count() == 0
    assert DailyCounter.objects.count() == 1  # created counter
    assert DailyCounter.objects.first().day == previous_date

    APIRequestLogFactory(user=None, viewset=None, service=None, requested_at=previous_date)
    [APIRequestLogFactory(user=None, viewset=None, service=None, requested_at=recent_date)
     for i in range(9)]

    assert APIRequestLog.objects.count() == 10
    assert DailyCounter.objects.count() == 1

    APIRequestLog.objects.aggregate()

    assert APIRequestLog.objects.count() == 9  # keep recent logs
    assert DailyCounter.objects.count() == 2  # created counter


def test_task(data, db):
    results = task_aggregate_log()
    assert results
