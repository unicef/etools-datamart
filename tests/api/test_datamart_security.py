import datetime

import pytest
from rest_framework.test import APIClient
from test_utilities.factories import AdminFactory, UserFactory, UserStatsFactory

from unicef_rest_framework.test_utils import user_allow_country, user_allow_service

from etools_datamart.api.endpoints import HACTViewSet, PartnerViewSet, UserStatsViewSet


@pytest.fixture()
def user(etools_user):
    return UserFactory(username=etools_user.username,
                       email=etools_user.email)


@pytest.fixture()
def local_user(db):
    return UserFactory()


@pytest.fixture()
def user_data(db):
    data = [UserStatsFactory(country_name='Lebanon', schema_name='lebanon', month=datetime.datetime(2000, 1, 1)),
            UserStatsFactory(country_name='Chad', schema_name='chad', month=datetime.datetime(2000, 1, 1)),
            UserStatsFactory(country_name='Bolivia', schema_name='bolivia', month=datetime.datetime(2000, 1, 1))]
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
def test_datamart_user_access_allowed_countries(admin_user, url, code, expected, user_data):
    client = APIClient()
    client.force_authenticate(admin_user)
    base = UserStatsViewSet.get_service().endpoint

    # with user_allow_service(user, UserStatsViewSet):
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
        res = client.get(f"{base}?country_name=lebanon,abc,xyz")
        assert res.status_code == 400, res
        assert res.json() == {'error': "Invalid schemas: abc,xyz",
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


@pytest.mark.parametrize("user_type,op,query,code,allowed", [(UserFactory, "=", "", 403, ""),
                                                             (UserFactory, "=", "", 200, "bolivia"),
                                                             (AdminFactory, "=", "", 200, ""),

                                                             (UserFactory, "=", "lebanon", 200, "lebanon"),
                                                             (UserFactory, "!=", "bolivia", 200, "lebanon"),
                                                             (UserFactory, "!=", "bolivia", 200, "lebanon"),
                                                             (UserFactory, "=", "lebanon", 403, "bolivia"),
                                                             (UserFactory, "=", "bolivia", 403, ""),
                                                             ])
def test_access(db, user_type, op, query, code, allowed):
    # etools user has access same countries as in eTools app
    user = user_type()
    client = APIClient()
    client.force_authenticate(user)
    url = HACTViewSet.get_service().endpoint
    with user_allow_service(user, HACTViewSet):
        with user_allow_country(user, allowed):
            res = client.get(f"{url}?country_name{op}{query}")
    assert res.status_code == code, res.content
