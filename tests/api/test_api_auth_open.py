
import pytest
from concurrency.api import disable_concurrency
from rest_framework.test import APIClient
from unicef_rest_framework.acl import ACL_ACCESS_LOGIN, ACL_ACCESS_OPEN

from etools_datamart.api.endpoints import PartnerViewSet


@pytest.fixture()
def service(db):
    service = PartnerViewSet.get_service()
    service.access = ACL_ACCESS_OPEN
    with disable_concurrency(service):
        service.save()
    yield service
    service.access = ACL_ACCESS_LOGIN
    service.save()


def test_loacl_user_access(anon_user, service):
    # etools user has access same countries as in eTools app
    client = APIClient()
    url = service.endpoint
    client.force_authenticate(anon_user)

    res = client.get(f"{url}?country_name=lebanon,chad")
    assert res.status_code == 403, res
    assert res.json() == {'error': "You are not allowed to access schema: 'chad,lebanon'"}
