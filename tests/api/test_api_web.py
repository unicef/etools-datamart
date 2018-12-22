# test BrowsableAPI
import pytest
from rest_framework.test import APIClient
from test_utilities.factories import UserFactory

from unicef_rest_framework.test_utils import user_allow_country, user_allow_service
from unicef_security.models import User

from etools_datamart.api.endpoints import (FAMIndicatorViewSet, InterventionViewSet,
                                           PMPIndicatorsViewSet, UserStatsViewSet,)


@pytest.fixture(autouse=True)
def users(db):
    UserFactory(username="user1")
    UserFactory(username="admin", is_superuser=True, is_staff=True)


@pytest.mark.parametrize("user", ("admin", "user1"))
def test_api_web_index(user):
    client = APIClient()
    client.force_authenticate(user)
    res = client.get('/api/latest/')
    assert res.status_code == 200, res.content


@pytest.mark.parametrize("username", ("admin", "user1"))
@pytest.mark.parametrize("viewset", [PMPIndicatorsViewSet, InterventionViewSet,
                                     FAMIndicatorViewSet, UserStatsViewSet])
def test_list_web(username, viewset):
    user = User.objects.get(username=username)
    client = APIClient()
    client.force_authenticate(user)
    with user_allow_country(user, "bolivia"):
        with user_allow_service(user, viewset):
            res = client.get(viewset.get_service().endpoint, HTTP_ACCEPT="text/html")
    assert res.status_code == 200, res.content
    assert res["Content-Type"] == "text/html; charset=utf-8"
