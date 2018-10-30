from datetime import datetime

import pytest
from test_utilities.factories import UserStatsFactory
from unicef_rest_framework.exceptions import InvalidQueryValueError

from etools_datamart.api.endpoints import UserStatsViewSet
from etools_datamart.api.endpoints.common import MonthFilterBackend


@pytest.fixture()
def data(db):
    today = datetime.today()
    return [UserStatsFactory(month=datetime(2018, 1, 1)),
            UserStatsFactory(month=datetime(2018, 2, 1)),
            UserStatsFactory(month=datetime(2018, 3, 1)),
            UserStatsFactory(month=datetime(2018, 4, 1)),
            UserStatsFactory(month=datetime(2018, today.month, 1)),
            ]


@pytest.mark.parametrize("month", [2, 'Feb', "2-2018", "Feb-2018", "current"])
def test_monthfilter(rf, data, month):
    view = UserStatsViewSet()
    request = rf.get("%s?month=%s" % (view.get_service().endpoint, month))
    bk = MonthFilterBackend()
    qs = bk.filter_queryset(request, view.get_queryset(), view)
    assert qs.count() == 1


def test_monthfilter_empty(rf, data):
    view = UserStatsViewSet()
    request = rf.get("%s?month=" % view.get_service().endpoint)
    bk = MonthFilterBackend()
    qs = bk.filter_queryset(request, view.get_queryset(), view)
    assert qs.count() == view.get_queryset().count()


@pytest.mark.parametrize("month", ["a", "-2000", "ùnïcòdé"])
def test_monthfilter_error(rf, data, month):
    view = UserStatsViewSet()
    request = rf.get("%s?month=abc" % view.get_service().endpoint)
    bk = MonthFilterBackend()
    with pytest.raises(InvalidQueryValueError):
        bk.filter_queryset(request, view.get_queryset(), view)
