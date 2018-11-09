from django.db import connections

from etools_datamart.apps.etools.models import UsersUserprofile
from etools_datamart.apps.multitenant.exceptions import InvalidSchema

conn = connections['etools']


def get_etools_allowed_schemas(user):
    # returns all allowed schemas as per eTools configuration
    # if `user` is also an eTools user.
    # matching is performed per email mnatching
    # TODO: manage non etools user permissions
    with conn.noschema():
        etools_user = UsersUserprofile.objects.filter(user__email=user.email).first()
        if etools_user:
            return set(etools_user.countries_available.values_list('schema_name', flat=True))
        else:
            return set()

#
# def schema_is_valid(*schema):
#     return schema in conn.all_schemas


def validate_schemas(*schemas):
    invalid = set(schemas) - conn.all_schemas
    if invalid:
        raise InvalidSchema(",".join(invalid))
