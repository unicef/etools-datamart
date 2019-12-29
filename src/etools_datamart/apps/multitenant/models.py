# -*- coding: utf-8 -*-
import logging

from django.db.models import *  # noqa
from django.db.models.manager import BaseManager

from .query import TenantQuerySet

logger = logging.getLogger(__name__)


class TenantManager(BaseManager.from_queryset(TenantQuerySet)):
    pass


class TenantModel(Model):  # noqa
    schema = CharField(db_column='__schema', max_length=100)  # noqa

    objects = TenantManager()

    def get_country_instance(self):
        from etools_datamart.apps.sources.etools.models import UsersCountry
        return UsersCountry.objects.get(schema_name=self.schema)

    class Meta:
        abstract = True
