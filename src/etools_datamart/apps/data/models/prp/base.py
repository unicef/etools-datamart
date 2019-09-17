from django.contrib.contenttypes.models import ContentType
from django.db import models

from celery.local import class_property

from etools_datamart.apps.data.loader import EtoolsLoader, EToolsLoaderOptions
from etools_datamart.apps.etl.base import DataMartModelBase


class PrpDataMartModelBase(DataMartModelBase):
    loader_option_class = EToolsLoaderOptions
    loader_class = EtoolsLoader


class PrpDataMartModel(models.Model, metaclass=PrpDataMartModelBase):
    source_id = models.IntegerField(blank=True, null=True, db_index=True)
    last_modify_date = models.DateTimeField(blank=True, auto_now=True)
    seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    @class_property
    def service(self):
        from unicef_rest_framework.models import Service
        return Service.objects.get(source_model=ContentType.objects.get_for_model(self))

    @class_property
    def linked_services(self):
        from unicef_rest_framework.models import Service
        return [s for s in Service.objects.all() if s.managed_model == self]
