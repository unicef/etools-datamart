import pytest
from rest_framework.test import APIClient
from test_utilities.factories import UserFactory
from unicef_rest_framework.test_utils import user_allow_service

from etools_datamart.api.endpoints import PartnerViewSet
from etools_datamart.apps.etools.models import AuthUser


@pytest.fixture()
def etools_user(db):
    return AuthUser.objects.get(id=1)


@pytest.fixture()
def user(etools_user):
    return UserFactory(username=etools_user.username,
                       email=etools_user.email)


@pytest.fixture()
def local_user(db):
    return UserFactory()


def test_etools_user_access_allowed_countries(user):
    # etools user has access same countries as in eTools app
    client = APIClient()
    client.force_authenticate(user)
    url = PartnerViewSet.get_service().endpoint

    with user_allow_service(user, PartnerViewSet):
        res = client.get(f"{url}")
        assert res.status_code == 200, res
        assert len(res.json()['results']) == 100

        res = client.get(f"{url}?country_name=lebanon")
        assert res.status_code == 200, res
        assert len(res.json()['results']) == 100

        res = client.get(f"{url}?country_name=lebanon,chad")
        assert res.status_code == 403, res
        assert res.json() == {'error': "You are not allowed to access schema: 'chad'"}


def test_loacl_user_access(local_user):
    # etools user has access same countries as in eTools app
    client = APIClient()
    client.force_authenticate(local_user)
    url = PartnerViewSet.get_service().endpoint

    with user_allow_service(local_user, PartnerViewSet):
        res = client.get(f"{url}")
        assert res.status_code == 403, res
        assert res.json() == {'error': "You don't have enbled schemas"}

        res = client.get(f"{url}?country_name=lebanon,chad")
        assert res.status_code == 403, res
        assert res.json() == {'error': "You are not allowed to access schema: 'chad,lebanon'"}
