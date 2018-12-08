from rest_framework.test import APIClient
from unicef_rest_framework.test_utils import user_allow_service

from etools_datamart.api.endpoints import PartnerViewSet


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

        res = client.get(f"{url}?country_name=lebanon,xxx")
        assert res.status_code == 400, res
        assert res.json() == {'error': "Invalid schema: 'xxx'",
                              'hint': 'Removes wrong schema from selection',
                              'valid': ['bolivia', 'chad', 'lebanon']}


def test_loacl_user_access(local_user):
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
