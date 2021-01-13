from unittest.mock import Mock

from etools_datamart.libs.impersonate import queryset


def test_queryset(admin_user, user):
    assert queryset(Mock(user=admin_user))
