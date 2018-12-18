from celery.local import class_property
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class DataMartQuerySet(QuerySet):

    def filter_schemas(self, *schemas):
        if schemas and schemas[0]:
            return self.filter(schema_name__in=schemas)
        return self


class DataMartManager(BaseManager.from_queryset(DataMartQuerySet)):
    pass
    # def truncate(self):
    #     self.raw('TRUNCATE TABLE {0}'.format(self.model._meta.db_table))


class DataMartModel(models.Model):
    country_name = models.CharField(max_length=50, db_index=True)
    area_code = models.CharField(max_length=10, db_index=True)
    schema_name = models.CharField(max_length=50, db_index=True)
    last_modify_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        abstract = True

    objects = DataMartManager()

    @class_property
    def service(self):
        from unicef_rest_framework.models import Service
        return Service.objects.get(source_model=ContentType.objects.get_for_model(self))

    @class_property
    def linked_services(self):
        from unicef_rest_framework.models import Service
        return [s for s in Service.objects.all() if s.managed_model == self]
