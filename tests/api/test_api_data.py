# -*- coding: utf-8 -*-
import pytest
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from test_utilities.factories import (FAMIndicatorFactory, HACTFactory, InterventionFactory,
                                      PMPIndicatorFactory, TaskLogFactory, UserStatsFactory,)

from etools_datamart.api.endpoints import (FAMIndicatorViewSet, HACTViewSet, InterventionViewSet,
                                           PMPIndicatorsViewSet, UserStatsViewSet,)
from etools_datamart.apps.data.models import FAMIndicator
from etools_datamart.apps.etl.models import EtlTask

VIEWSETS = [
    FAMIndicatorViewSet,
    HACTViewSet,
    InterventionViewSet,
    PMPIndicatorsViewSet,
    UserStatsViewSet,
]

FORMATS = (('', 'application/json'),
           ('csv', 'text/csv; charset=utf-8'),
           ('xml', 'application/xml; charset=utf-8'),
           # ('html', 'text/html; charset=utf-8'),
           ('json', 'application/json'),
           ('ms-xml', 'application/xml; charset=utf-8'),
           ('ms-json', 'application/json'),
           ('csv', 'text/csv; charset=utf-8'),
           ('pdf', 'application/pdf; charset=utf-8'),
           ('xlsx', 'application/xlsx; charset=utf-8'),
           )


@pytest.fixture()
def data(db):
    EtlTask.objects.inspect()
    data = [
        FAMIndicatorFactory(),
        HACTFactory(),
        InterventionFactory(),
        PMPIndicatorFactory(),
        UserStatsFactory(),
    ]
    yield
    [r.delete() for r in data]


@pytest.mark.parametrize("action", ['', 'updates/'])
@pytest.mark.parametrize("format,ct", FORMATS)
@pytest.mark.parametrize("viewset", VIEWSETS)
def test_list(client, action, viewset, format, ct, data):
    res = client.get(f"{viewset.get_service().endpoint}{action}?format={format}")
    assert res.status_code == 200, res
    assert res.content
    assert res['Content-Type'] == ct


def test_updates(client):
    viewset = FAMIndicatorViewSet()
    TaskLogFactory(last_changes=timezone.now(),
                   content_type=ContentType.objects.get_for_model(FAMIndicator))

    url = f"{viewset.get_service().endpoint}updates/"
    res = client.get(url)
    assert res.status_code == 200, res

# @pytest.mark.parametrize("viewset", VIEWSETS)
# def test_list_json(client, viewset):
#     res = client.get(viewset.get_service().endpoint)
#     assert res.status_code == 200, res
#     assert res.json()
#
#
# @pytest.mark.parametrize("viewset", VIEWSETS)
# def test_list_csv(client, viewset, data):
#     res = client.get(f"{viewset.get_service().endpoint}?format=csv", format='csv')
#     assert res.status_code == 200, res
#     assert res['Content-Type'] == "text/csv; charset=utf-8"
#
#
# @pytest.mark.parametrize("viewset", VIEWSETS)
# def test_list_xml(client, viewset):
#     res = client.get(f"{viewset.get_service().endpoint}?format=xml", format='xml')
#     assert res.status_code == 200, res
#
#
# @pytest.mark.parametrize("viewset", VIEWSETS)
# def test_list_msxml(client, viewset):
#     res = client.get(f"{viewset.get_service().endpoint}?format=ms-xml", format='ms-xml')
#     assert res.status_code == 200, res
#
#
# @pytest.mark.parametrize("viewset", VIEWSETS)
# def test_list_msjson(client, viewset):
#     res = client.get(f"{viewset.get_service().endpoint}?format=ms-json", format='ms-json')
#     assert res.status_code == 200, res
#     assert res.json()
#
#
# @pytest.mark.parametrize("viewset", VIEWSETS)
# def test_updates(client, viewset):
#     res = client.get(f"{viewset.get_service().endpoint}/updates/?format=ms-json", format='ms-json')
#     assert res.status_code == 200, res
#     assert res.json()
