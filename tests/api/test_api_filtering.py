import pytest
from rest_framework.test import APIClient
from unicef_rest_framework.test_utils import user_allow_country, user_allow_service

from etools_datamart.api.endpoints import InterventionViewSet


@pytest.mark.parametrize('flt', ['country_name=bolivia', 'country_name=', 'country_name=bolivia,chad'])
def test_filter_etools_country_name(db, client, flt):
    url = f"/api/latest/etools/audit/engagement/?%s" % flt
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()


@pytest.mark.parametrize('flt', ['country_name=bolivia', 'country_name=', 'country_name=bolivia,chad'])
def test_filter_datamart_country_name_admin(db, client, flt):
    url = f"/api/latest/datamart/interventions/?%s" % flt
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()


@pytest.mark.parametrize('flt', ['country_name=lebanon', 'country_name=', 'country_name=lebanon,chad'])
def test_filter_datamart_country_name_uset(user, flt):
    client = APIClient()
    client.force_authenticate(user)
    base = InterventionViewSet.get_service().endpoint

    with user_allow_country(user, ['lebanon', 'chad']):
        with user_allow_service(user, InterventionViewSet):
            url = f"{base}?{flt}"
            res = client.get(url)
            assert res.status_code == 200
            assert res.json()


@pytest.mark.parametrize('flt', ['10', 'oct', '10-2018', 'current', ''])
def test_filter_datamart_month(db, client, flt):
    url = f"/api/latest/datamart/user-stats/?month=%s" % flt
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()

#
# @pytest.mark.parametrize('flt', ['10', 'oct', '10-2018', 'current', ''])
# def test_filter_datamart_month(user, flt):
#     with user_allow_service(user, PartnerViewSet):
#     url = f"/api/latest/datamart/user-stats/?month=%s" % flt
#     res = client.get(url)
#     assert res.status_code == 200
#     assert res.json()
