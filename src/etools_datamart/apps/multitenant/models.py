import logging

from django.core.cache import cache
from django.db.models import *  # noqa
from django.db.models.manager import BaseManager

from .query import TenantQuerySet

logger = logging.getLogger(__name__)


class TenantManager(BaseManager.from_queryset(TenantQuerySet)):
    pass


class TenantModel(Model):  # noqa
    schema = CharField(db_column="__schema", max_length=100)  # noqa

    objects = TenantManager()

    def get_user_country(self, schema_name):
        from etools_datamart.apps.sources.etools.models import UsersCountry

        cache_key = f"user_country_{schema_name}"
        user_country = cache.get(cache_key)
        if user_country is None:
            user_country = UsersCountry.objects.get(schema_name=schema_name)
            cache.set(cache_key, user_country)
        return user_country

    def get_country_instance(self):
        # from etools_datamart.apps.sources.etools.models import UsersCountry
        # return UsersCountry.objects.get(schema_name=self.schema)
        return self.get_user_country(self.schema)

    class Meta:
        abstract = True
