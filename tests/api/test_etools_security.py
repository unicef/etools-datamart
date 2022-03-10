import pytest
from rest_framework.test import APIClient
from test_utilities.factories import AdminFactory, UserFactory

from unicef_rest_framework.test_utils import user_allow_country, user_allow_service

from etools_datamart.api.endpoints import PartnerViewSet

# def test_etools_user_access_allowed_countries(user):
#     # etools user has access same countries as in eTools app
#     client = APIClient()
#     client.force_authenticate(user)
#     url = PartnerViewSet.get_service().endpoint
#
#     with user_allow_service(user, PartnerViewSet):
#         res = client.get(f"{url}")
#         assert res.status_code == 200, res
#         assert len(res.json()['results']) == 100
#
#         res = client.get(f"{url}?country_name=lebanon")
#         assert res.status_code == 200, res
#         assert len(res.json()['results']) == 100
#
#         res = client.get(f"{url}?country_name=lebanon,chad")
#         assert res.status_code == 403, res
#         assert res.json() == {'error': "You are not allowed to access schema: 'chad'"}
#
#         res = client.get(f"{url}?country_name=lebanon,xxx")
#         assert res.status_code == 400, res
#         assert res.json() == {'error': "Invalid schema: xxx",
#                               'hint': 'Removes wrong schema from selection',
#                               'valid': ['bolivia', 'chad', 'lebanon']}


def pytest_generate_tests(metafunc):
    if 'params' in metafunc.fixturenames:
        ret, ids = [], []
        ret.append([UserFactory, PartnerViewSet, 200])
        ids.append("UserFactory, PartnerViewSet, 200")

        ret.append([AdminFactory, PartnerViewSet, 200])
        ids.append("AdminFactory, PartnerViewSet, 200")
        metafunc.parametrize("params", ret, ids=ids)


@pytest.mark.django_db
def test_etools_user_access_allowed_countries(params):
    # etools user has access same countries as in eTools app
    user_type, viewset, code = params
    user = user_type()
    url = viewset.get_service().endpoint

    client = APIClient()
    client.force_authenticate(user)
    # url = PartnerViewSet.get_service().endpoint
    #
    with user_allow_service(user, viewset):
        with user_allow_country(user, "bolivia"):
            res = client.get(f"{url}")
            assert res.status_code == code, res.content
    #     assert len(res.json()['results']) == 100
    #
    #     res = client.get(f"{url}?country_name=lebanon")
    #     assert res.status_code == 200, res
    #     assert len(res.json()['results']) == 100
    #
    #     res = client.get(f"{url}?country_name=lebanon,chad")
    #     assert res.status_code == 403, res
    #     assert res.json() == {'error': "You are not allowed to access schema: 'chad'"}
    #
    #     res = client.get(f"{url}?country_name=lebanon,xxx")
    #     assert res.status_code == 400, res
    #     assert res.json() == {'error': "Invalid schema: xxx",
    #                           'hint': 'Removes wrong schema from selection',
    #                           'valid': ['bolivia', 'chad', 'lebanon']}


@pytest.mark.parametrize("user_type,op,query,code,allowed", [
    # (UserFactory, "=", "", 403, ""),
    (UserFactory, "=", "", 200, "bolivia"),
    (AdminFactory, "=", "", 200, ""),
    (UserFactory, "=", "lebanon", 200, "lebanon"),
    (UserFactory, "!=", "bolivia", 200, "lebanon"),
    (UserFactory, "!=", "bolivia", 200, "lebanon"),
    # (UserFactory, "=", "lebanon", 403, "bolivia"),
    (UserFactory, "=", "bolivia", 403, ""),
])
def test_access(db, user_type, op, query, code, allowed):
    # etools user has access same countries as in eTools app
    user = user_type()
    client = APIClient()
    client.force_authenticate(user)
    url = PartnerViewSet.get_service().endpoint
    with user_allow_service(user, PartnerViewSet):
        with user_allow_country(user, allowed):
            res = client.get(f"{url}?country_name{op}{query}")
            assert res.status_code == code, res.content
            # assert res.json() == {'error': "You don't have enabled schemas"}
        #
        # with user_allow_country(local_user, ['bolivia']):
        #     res = client.get(f"{url}?country_name=lebanon,chad")
        #     assert res.status_code == 403, res.content
        #     assert res.json() == {'error': "You are not allowed to access schema: 'chad,lebanon'"}
        #
        # with user_allow_country(local_user, ['lebanon']):
        #     res = client.get(f"{url}")
        #     assert res.status_code == 200, res.content
