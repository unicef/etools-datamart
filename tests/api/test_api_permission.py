# -*- coding: utf-8 -*-
import pytest
from rest_framework.test import APIClient
from unicef_rest_framework.models import Service, UserAccessControl


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    return client


@pytest.fixture()
def allow(user1, service):
    from test_utilities.factories import UserAccessControlFactory
    return UserAccessControlFactory(policy=UserAccessControl.POLICY_ALLOW,
                                    service=service,
                                    user=user1)


@pytest.fixture()
def deny(user1, service):
    from test_utilities.factories import UserAccessControlFactory
    return UserAccessControlFactory(policy=UserAccessControl.POLICY_DENY,
                                    service=service,
                                    user=user1)


@pytest.fixture()
def service(db):
    Service.objects.load_services()
    return Service.objects.order_by('?').first()


def test_permission_deny(client, deny):
    url = deny.service.endpoint
    client.force_authenticate(deny.user)

    res = client.get(url, HTTP_X_SCHEMA="bolivia")
    assert res.status_code == 403


def test_permission_allow(client, allow):
    url = allow.service.endpoint
    client.force_authenticate(allow.user)

    res = client.get(url, HTTP_X_SCHEMA="bolivia")
    assert res.status_code == 200
