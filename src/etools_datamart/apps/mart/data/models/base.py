from django.contrib.contenttypes.models import ContentType
from django.db import models

from celery.local import class_property

# from etools_datamart.apps.mart.data import (CommonSchemaLoader, CommonSchemaLoaderOptions,
#                                             EtoolsLoader, EToolsLoaderOptions, )
from etools_datamart.apps.core.models import DataMartManager
from etools_datamart.apps.etl.base import DataMartModelBase
from etools_datamart.apps.mart.data.loader import (
    CommonSchemaLoader,
    CommonSchemaLoaderOptions,
    EtoolsLoader,
    EToolsLoaderOptions,
)


class CommonDataMartModelModelBase(DataMartModelBase):
    loader_option_class = CommonSchemaLoaderOptions
    loader_class = CommonSchemaLoader


class EToolsDataMartModelBase(CommonDataMartModelModelBase):
    loader_option_class = EToolsLoaderOptions
    loader_class = EtoolsLoader


class CommonDataMartModel(models.Model, metaclass=CommonDataMartModelModelBase):
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


class EtoolsDataMartModel(CommonDataMartModel, metaclass=EToolsDataMartModelBase):
    country_name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, db_index=True)
    area_code = models.CharField(max_length=10, db_index=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['source_id', 'schema_name']),
        ]

    objects = DataMartManager()
