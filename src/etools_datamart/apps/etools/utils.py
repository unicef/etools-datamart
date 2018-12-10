from functools import lru_cache

from django.db import connections
from unicef_security.models import Role

from etools_datamart.apps.etools.models import UsersUserprofile

conn = connections['etools']


@lru_cache()
def get_allowed_schemas(user):
    # returns all allowed schemas
    if user.is_superuser:
        return conn.all_schemas
    with conn.noschema():
        aa = list(Role.objects.filter(user=user).values_list('business_area__name', flat=True))
        etools_user = UsersUserprofile.objects.filter(user__email=user.email).first()
        if etools_user:
            aa.extend(set(etools_user.countries_available.values_list('schema_name', flat=True)))

    return set(filter(None, aa))
    # return set(map(lambda s: s.lower(), aa))
#
# def schema_is_valid(*schema):
#     return schema in conn.all_schemas


# def validate_schemas(*schemas):
#     invalid = set(schemas) - conn.all_schemas
#     if invalid:
#         raise InvalidSchema(",".join(invalid))
