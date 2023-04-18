import pytest
from rest_framework.test import APIClient
from test_utilities.factories import AdminFactory, FAMIndicatorFactory, FundsReservationFactory, UserFactory

from unicef_rest_framework.test_utils import user_allow_country, user_allow_service

from etools_datamart.api.endpoints import EtoolsAssessmentViewSet, InterventionViewSet, PartnerViewSet


class MockCache:
    data = {}

    def set(self, key, value, *args, **kwargs):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)


@pytest.fixture()
def client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.mark.parametrize("flt", ["country_name=bolivia", "country_name=bolivia,chad", "country_name=BOL,0810"])
def test_filter_cache_country_arg(db, client, flt, monkeypatch):
    fake = MockCache()
    monkeypatch.setattr("etools_datamart.api.filtering.cache", fake)
    url = f"/api/latest/sources/etools/partners/assessment/?%s" % flt
    with user_allow_service(client.handler._force_user, EtoolsAssessmentViewSet):
        with user_allow_country(client.handler._force_user, ["bolivia", "chad"]):
            client.get(url)
            res = client.get(url)
    assert fake.data
    assert res.status_code == 200, res.content
    assert res.json()


# @pytest.mark.django_db
# @pytest.mark.parametrize('user_type', [UserFactory, AdminFactory])
# @pytest.mark.parametrize('viewset', [PartnerViewSet, InterventionViewSet])
# @pytest.mark.parametrize('flt', ['bolivia', 'bolivia,chad', 'BOL,0810'])
# @pytest.mark.parametrize('op', ['=', '!='])
# def test_filter_country(flt, viewset, user_type, op):
#     user = user_type()
#     client = APIClient()
#     client.force_authenticate(user)
#     service = viewset.get_service()
#     schemas = get_schema_names(flt)
#     url = f"{service.endpoint}?country_name{op}{flt}"
#     with user_allow_country(user, schemas):
#         with user_allow_service(user, viewset):
#             res = client.get(url)
#     assert res.status_code == 200, res.content
#     assert res.json()


@pytest.mark.django_db
@pytest.mark.parametrize("user_type", [UserFactory, AdminFactory])
@pytest.mark.parametrize("viewset", [PartnerViewSet, InterventionViewSet])
@pytest.mark.parametrize("op", ["=", "!="])
def test_filter_country_invalid(viewset, user_type, op):
    user = user_type()
    client = APIClient()
    client.force_authenticate(user)
    service = viewset.get_service()
    url = f"{service.endpoint}?country_name{op}aaa"
    with user_allow_service(user, viewset):
        res = client.get(url)
    assert res.status_code == 400


#
# @pytest.mark.parametrize('flt', ['country_name=bolivia', 'country_name=', 'country_name=bolivia,chad'])
# def test_filter_etools_country_name(db, client, flt):
#     url = f"/api/latest/etools/audit/engagement/?%s" % flt
#     with user_allow_service(client.handler._force_user, AuditEngagement):
#         res = client.get(url)
#     assert res.status_code == 200
#     assert res.json()
#
#
# @pytest.mark.parametrize('flt', ['country_name=bolivia', 'country_name=', 'country_name=bolivia,chad'])
# def test_filter_datamart_country_name_admin(db, client, flt):
#     url = f"/api/latest/datamart/interventions/?%s" % flt
#     with user_allow_service(client.handler._force_user, InterventionViewSet):
#         res = client.get(url)
#     assert res.status_code == 200
#     assert res.json()
#
#
# @pytest.mark.parametrize('flt', ['country_name=lebanon', 'country_name=', 'country_name=lebanon,chad',
#                                  'country_name=LEBA,0810'])
# def test_filter_datamart_country_name_uset(user, flt):
#     client = APIClient()
#     client.force_authenticate(user)
#     base = InterventionViewSet.get_service().endpoint
#
#     with user_allow_country(user, ['lebanon', 'chad']):
#         with user_allow_service(user, InterventionViewSet):
#             url = f"{base}?{flt}"
#             res = client.get(url)
#             assert res.status_code == 200
#             assert res.json()
#
#


@pytest.mark.parametrize("ct", ["text/html", "application/json"])
@pytest.mark.parametrize("flt", ["10", "oct", "10-2018", "current", "", "12-"])
def test_filter_datamart_month(db, client, flt, ct):
    FAMIndicatorFactory(month="2018-12")
    client.force_authenticate(AdminFactory())

    url = f"/api/latest/datamart/fam-indicators/?month=%s" % flt
    res = client.get(url, HTTP_ACCEPT=ct)
    assert res.status_code == 200
    # assert res.json()


@pytest.mark.parametrize("ct", ["text/html", "application/json"])
@pytest.mark.parametrize("flt", ["2000-01-01"])
def test_filter_datamart_fundsreservation(db, client, flt, ct):
    FundsReservationFactory()
    client.force_authenticate(AdminFactory())

    url = f"/api/latest/datamart/funds-reservation/?start_date__gt=%s" % flt
    res = client.get(url, HTTP_ACCEPT=ct)
    assert res.status_code == 200
    # assert res.json()


#
# @pytest.mark.parametrize('flt', ['10', 'oct', '10-2018', 'current', '', '10-'])
# def test_filter_datamart_month_browseable(admin_user, django_app, flt):
#     url = f"/api/latest/datamart/user-stats/?month=%s" % flt
#     res = django_app.get(url, user=admin_user, HTTP_ACCEPT='text/html')
#     assert res.status_code == 200
#     assert res.content == ""
#

#
# @pytest.mark.parametrize('flt', ['10', 'oct', '10-2018', 'current', ''])
# def test_filter_datamart_month(user, flt):
#     with user_allow_service(user, PartnerViewSet):
#     url = f"/api/latest/datamart/user-stats/?month=%s" % flt
#     res = client.get(url)
#     assert res.status_code == 200
#     assert res.json()
