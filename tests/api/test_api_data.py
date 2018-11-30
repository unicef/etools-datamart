# -*- coding: utf-8 -*-
import pytest
from test_utilities.factories import (FAMIndicatoFactory, HACTFactory, InterventionFactory,
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


@pytest.mark.parametrize("viewset", [PMPIndicatorsViewSet, InterventionViewSet,
                                     FAMIndicatorViewSet, UserStatsViewSet])
def test_list_xml(client, viewset):
    res = client.get(f"{viewset.get_service().endpoint}?format=xml", format='xml')
    assert res.status_code == 200, res


@pytest.mark.parametrize("viewset", [PMPIndicatorsViewSet, InterventionViewSet,
                                     FAMIndicatorViewSet, UserStatsViewSet])
def test_list_msxml(client, viewset):
    res = client.get(f"{viewset.get_service().endpoint}?format=ms-xml", format='ms-xml')
    assert res.status_code == 200, res


@pytest.mark.parametrize("viewset", [PMPIndicatorsViewSet, InterventionViewSet,
                                     FAMIndicatorViewSet, UserStatsViewSet])
def test_list_msjson(client, viewset):
    res = client.get(f"{viewset.get_service().endpoint}?format=ms-json", format='ms-json')
    assert res.status_code == 200, res
    assert res.json()
