from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from unicef_security.models import TimeStampedModel


class DataMartQuerySet(QuerySet):

    def filter_schemas(self, *schemas):
        if schemas and schemas[0]:
            return self.filter(schema_name__in=schemas)
        return self


class DataMartManager(BaseManager.from_queryset(DataMartQuerySet)):
    def truncate(self):
        self.raw('TRUNCATE TABLE {0}'.format(self.model._meta.db_table))


class DataMartModel(models.Model, TimeStampedModel):
    country_name = models.CharField(max_length=50, db_index=True)
    schema_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        abstract = True

    objects = DataMartManager()
