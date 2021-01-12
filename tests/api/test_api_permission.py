from django.utils.http import urlquote

import pytest
from rest_framework.test import APIClient
from test_utilities.factories import InterventionFactory

from unicef_rest_framework.models import UserAccessControl
from unicef_rest_framework.test_utils import user_allow_country

from etools_datamart.api.endpoints import InterventionViewSet


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    return client


@pytest.fixture()
def allow(user1):
    service = InterventionViewSet.get_service()

    from test_utilities.factories import UserAccessControlFactory
    return UserAccessControlFactory(policy=UserAccessControl.POLICY_ALLOW,
                                    service=service,
                                    user=user1)


@pytest.fixture()
def allow_std_serializer(user1):
    service = InterventionViewSet.get_service()
    InterventionFactory()
    from test_utilities.factories import UserAccessControlFactory
    acl = UserAccessControlFactory(policy=UserAccessControl.POLICY_ALLOW,
                                   service=service,
                                   serializers=["std"],
                                   user=user1)
    yield acl
    acl.delete()


@pytest.fixture()
def allow_any_serializer(user1):
    service = InterventionViewSet.get_service()
    InterventionFactory()
    from test_utilities.factories import UserAccessControlFactory
    acl = UserAccessControlFactory(policy=UserAccessControl.POLICY_ALLOW,
                                   service=service,
                                   serializers=["*"],
                                   user=user1)
    yield acl
    acl.delete()


@pytest.fixture()
def allow_many_serializer(user1):
    service = InterventionViewSet.get_service()
    InterventionFactory()
    from test_utilities.factories import UserAccessControlFactory
    acl = UserAccessControlFactory(policy=UserAccessControl.POLICY_ALLOW,
                                   service=service,
                                   serializers=["std", "short"],
                                   user=user1)
    yield acl
    acl.delete()


@pytest.fixture()
def deny(user1, service):
    from test_utilities.factories import UserAccessControlFactory
    acl = UserAccessControlFactory(policy=UserAccessControl.POLICY_DENY,
                                   service=service,
                                   user=user1)
    yield acl
    acl.delete()


@pytest.mark.django_db()
def test_permission_deny(client, deny):
    url = deny.service.endpoint
    client.force_authenticate(deny.user)

    res = client.get(url, HTTP_X_SCHEMA="bolivia")
    assert res.status_code == 403


def test_permission_allow(client, allow):
    url = allow.service.endpoint
    client.force_authenticate(allow.user)
    with user_allow_country(allow.user, 'bolivia'):
        res = client.get(url)
    assert res.status_code == 200


def test_permission_check_serializer_allow(client, allow_many_serializer):
    url = allow_many_serializer.service.endpoint
    view = allow_many_serializer.service.viewset
    client.force_authenticate(allow_many_serializer.user)
    with user_allow_country(allow_many_serializer.user, 'bolivia'):
        res = client.get("%s?%s=short" % (url, urlquote(view.serializer_field_param)))
    assert res.status_code == 200
    # assert res.json()['detail'] == "You do not have permission to perform this action."


def test_permission_check_serializer_deny(client, allow_std_serializer):
    url = allow_std_serializer.service.endpoint
    view = allow_std_serializer.service.viewset
    client.force_authenticate(allow_std_serializer.user)
    # with user_allow_country(allow_many_serializer.user, 'bolivia'):
    res = client.get("%s?%s=short" % (url, urlquote(view.serializer_field_param)))
    assert res.status_code == 403, res.content
    assert res.json()['error'] == "Forbidden serializer 'short'"


def test_permission_check_serializer_any(client, allow_any_serializer):
    url = allow_any_serializer.service.endpoint
    view = allow_any_serializer.service.viewset
    client.force_authenticate(allow_any_serializer.user)
    with user_allow_country(allow_any_serializer.user, 'bolivia'):
        res = client.get("%s?%s=short" % (url, urlquote(view.serializer_field_param)))
    assert res.status_code == 200, res.content


def test_permission_check_user(client, allow_any_serializer, user2):
    url = allow_any_serializer.service.endpoint
    view = allow_any_serializer.service.viewset
    client.force_authenticate(user2)

    res = client.get("%s?%s=short" % (url, urlquote(view.serializer_field_param)))
    assert res.status_code == 403
