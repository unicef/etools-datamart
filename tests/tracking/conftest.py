import json

import pytest
from test_utilities.factories import APIRequestLogFactory

from etools_datamart.apps.core.models import User


@pytest.fixture
def system_user(db):
    return User.objects.get(username="system")


@pytest.fixture
def log(db):
    return APIRequestLogFactory()


@pytest.fixture
def log_with_params(db):
    return APIRequestLogFactory(query_params=json.dumps({"a": 1}))


@pytest.fixture
def reset_stats(db):
    from etools_datamart.apps.tracking.models import (
        APIRequestLog,
        DailyCounter,
        MonthlyCounter,
        PathCounter,
        UserCounter,
    )
    from etools_datamart.apps.tracking.utils import refresh_all_counters

    APIRequestLog.objects.truncate()
    DailyCounter.objects.truncate()
    MonthlyCounter.objects.truncate()
    PathCounter.objects.truncate()
    UserCounter.objects.truncate()
    refresh_all_counters()
