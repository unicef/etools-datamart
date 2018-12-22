from django.core.cache import caches
from django.db import connections

from concurrency.utils import flatten
from constance import config

from unicef_rest_framework.models import Service

from etools_datamart.apps.etools.models import UsersUserprofile
from etools_datamart.apps.security.models import SchemaAccessControl
from etools_datamart.libs.version import get_full_version

conn = connections['etools']
cache = caches['default']


def get_allowed_schemas(user):
    key = f"allowed_schemas:{get_full_version()}:{config.CACHE_VERSION}:{user.pk}"
    values = cache.get(key)
    if not values:
        if config.DISABLE_SCHEMA_RESTRICTIONS:
            values = conn.all_schemas
        elif not user.is_authenticated:
            values = []
        elif user.is_superuser:
            values = conn.all_schemas
        else:
            with conn.noschema():
                aa = flatten(list(SchemaAccessControl.objects.filter(group__user=user).values_list('schemas')))
                etools_user = UsersUserprofile.objects.filter(user__email=user.email).first()
                if etools_user:
                    aa.extend(set(etools_user.countries_available.values_list('schema_name', flat=True)))
            values = list(filter(None, aa))
        cache.set(key, list(values))
    return set(values)
    # return set(map(lambda s: s.lower(), aa))


def get_allowed_services(user):
    if not user.is_authenticated:
        return []
    if user.is_superuser or config.DISABLE_SERVICE_RESTRICTIONS:
        return Service.objects.all()
    return Service.objects.filter(groupaccesscontrol__group__user=user)

# def schema_is_valid(*schema):
#     return schema in conn.all_schemas


# def validate_schemas(*schemas):
#     invalid = set(schemas) - conn.all_schemas
#     if invalid:
#         raise InvalidSchema(",".join(invalid))
