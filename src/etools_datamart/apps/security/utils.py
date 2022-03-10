from functools import lru_cache

from django.conf import settings
from django.core.cache import caches
from django.db import connections

from concurrency.utils import flatten
from constance import config

from unicef_rest_framework.models import Service

from etools_datamart.apps.security.models import SchemaAccessControl
from etools_datamart.apps.sources.etools.models import UsersUserprofile
from etools_datamart.libs.version import get_full_version

conn = connections['etools']
cache = caches['default']


@lru_cache(2)
def get_allowed_schemas(user):
    if not user.is_authenticated:
        return []
    key = f"allowed_schemas:{get_full_version()}:{config.CACHE_VERSION}:{user.pk}"
    values = cache.get(key)
    if not values:  # pragma: no branch
        if user.is_superuser:
            values = conn.all_schemas
        else:
            with conn.noschema():
                aa = flatten(list(SchemaAccessControl.objects.filter(group__user=user).values_list('schemas')))
                etools_user = UsersUserprofile.objects.filter(user_id=user.pk).first()
                if etools_user:
                    etools_allowed = etools_user.UsersUserprofileCountriesAvailable_userprofile.exclude(
                        **settings.SCHEMA_EXCLUDE)
                    aa.extend(set(etools_allowed.values_list('country__schema_name', flat=True)))
            values = list(filter(None, aa))
        cache.set(key, list(values))
    return set(values)
    # return set(map(lambda s: s.lower(), aa))


def get_allowed_services(user):
    if not user.is_authenticated:  # pragma: no cover
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
