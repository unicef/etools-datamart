from django.contrib.contenttypes.models import ContentType
from django.db import connections, models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from celery.local import class_property

from etools_datamart.apps.data.loader import EtoolsLoader, EToolsLoaderOptions
from etools_datamart.apps.etl.base import DataMartModelBase


class DataMartQuerySet(QuerySet):
    def get(self, *args, **kwargs):
        try:
            return super(DataMartQuerySet, self).get(*args, **kwargs)
        except self.model.DoesNotExist as e:
            raise self.model.DoesNotExist(
                "%s  (%s %s)" % (e, args, kwargs)
            )
        except self.model.MultipleObjectsReturned as e:  # pragma: no cover
            raise self.model.MultipleObjectsReturned(
                "%s (%s %s) " % (e, args, kwargs)
            )

    def filter_schemas(self, *schemas):
        if schemas and schemas[0]:
            return self.filter(schema_name__in=schemas)
        return self


class DataMartManager(BaseManager.from_queryset(DataMartQuerySet)):

    def truncate(self, reset=True):
        if reset:
            restart = 'RESTART IDENTITY'
        else:
            restart = ''
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" {1} CASCADE;'.format(self.model._meta.db_table,
                                                                      restart))


class EToolsDataMartModelBase(DataMartModelBase):
    loader_option_class = EToolsLoaderOptions
    loader_class = EtoolsLoader


class CommonDataMartModel(models.Model, metaclass=DataMartModelBase):
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
