# -*- coding: utf-8 -*-
import pytest
from tests._test_lib.test_utilities.factories import (FAMIndicatoFactory, HACTFactory, InterventionFactory,
                                                      PMPIndicatorFactory, UserStatsFactory,)

from etools_datamart.api.endpoints import (FAMIndicatorViewSet, InterventionViewSet,
                                           PMPIndicatorsViewSet, UserStatsViewSet,)


@pytest.fixture()
def data(db):
    data = [HACTFactory(),
            PMPIndicatorFactory(),
            FAMIndicatoFactory(),
            InterventionFactory(),
            UserStatsFactory()]
    yield
    [r.delete() for r in data]


@pytest.mark.parametrize("viewset", [PMPIndicatorsViewSet, InterventionViewSet,
                                     FAMIndicatorViewSet, UserStatsViewSet])
def test_list_json(client, viewset):
    res = client.get(viewset.get_service().endpoint)
    assert res.status_code == 200, res
    assert res.json()


@pytest.mark.parametrize("viewset", [PMPIndicatorsViewSet, InterventionViewSet,
                                     FAMIndicatorViewSet, UserStatsViewSet])
def test_list_csv(client, viewset, data):
    res = client.get(f"{viewset.get_service().endpoint}?format=csv", format='csv')
    assert res.status_code == 200, res
    assert res['Content-Type'] == "text/csv; charset=utf-8"
