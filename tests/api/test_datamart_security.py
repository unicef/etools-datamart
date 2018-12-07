import datetime

import pytest
from rest_framework.test import APIClient
from test_utilities.factories import UserFactory, UserStatsFactory
from unicef_rest_framework.test_utils import user_allow_service

from etools_datamart.api.endpoints import PartnerViewSet, UserStatsViewSet


@pytest.fixture()
def user(etools_user):
    return UserFactory(username=etools_user.username,
                       email=etools_user.email)


@pytest.fixture()
def local_user(db):
    return UserFactory()


@pytest.fixture()
def user_data(db):
    data = [UserStatsFactory(country_name='lebanon', month=datetime.datetime(2000, 1, 1)),
            UserStatsFactory(country_name='chad', month=datetime.datetime(2000, 1, 1)),
            UserStatsFactory(country_name='bolivia', month=datetime.datetime(2000, 1, 1))]
    yield
    [r.delete() for r in data]


PARAMS = [("", 200, 3),
          ("country_name=lebanon", 200, 1),
          ("country_name!=lebanon", 200, 2),
          ]


@pytest.mark.parametrize("url,code,expected",
                         PARAMS,
                         ids=[p[0] for p in PARAMS]
                         )
def test_datamart_user_access_allowed_countries(user, url, code, expected, user_data):
    client = APIClient()
    client.force_authenticate(user)
    base = UserStatsViewSet.get_service().endpoint

    with user_allow_service(user, UserStatsViewSet):
        res = client.get(f"{base}?{url}")
        assert res.status_code == code, res
        assert len(res.json()['results']) == expected, res.json()


def test_datamart_user_access_forbidden_countries(user, user_data):
    client = APIClient()
    client.force_authenticate(user)
    base = UserStatsViewSet.get_service().endpoint
    with user_allow_service(user, UserStatsViewSet):
        res = client.get(f"{base}?country_name=lebanon,chad")
        assert res.status_code == 403, res
        assert res.json() == {'error': "You are not allowed to access schema: 'chad'"}


def test_datamart_user_access_wrong_countries(user, user_data):
    client = APIClient()
    client.force_authenticate(user)
    base = UserStatsViewSet.get_service().endpoint
    with user_allow_service(user, UserStatsViewSet):
        res = client.get(f"{base}?country_name=lebanon,xxx")
        assert res.status_code == 400, res
        assert res.json() == {'error': "Invalid schema: 'xxx'",
                              'hint': 'Removes wrong schema from selection',
                              'valid': ['bolivia', 'chad', 'lebanon']}


def test_local_user_access(local_user, user_data):
    # etools user has access same countries as in eTools app
    client = APIClient()
    client.force_authenticate(local_user)
    url = PartnerViewSet.get_service().endpoint

    with user_allow_service(local_user, PartnerViewSet):
        res = client.get(f"{url}")
        assert res.status_code == 403, res
        assert res.json() == {'error': "You don't have enabled schemas"}

        res = client.get(f"{url}?country_name=lebanon,chad")
        assert res.status_code == 403, res
        assert res.json() == {'error': "You are not allowed to access schema: 'chad,lebanon'"}
