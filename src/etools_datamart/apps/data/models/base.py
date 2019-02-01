from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.db.models.base import ModelBase
from django.db.models.manager import BaseManager

from celery.local import class_property

from etools_datamart.apps.data.loader import Loader, LoaderOptions


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

    def truncate(self):
        self.raw('TRUNCATE TABLE {0} CASCADE'.format(self.model._meta.db_table))


class DataMartModelBase(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, DataMartModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        loader = attrs.pop('loader', None)
        config = attrs.pop('Options', None)

        new_class = super_new(cls, name, bases, attrs, **kwargs)
        if not loader:  # no custom loader use default
            loader = Loader()
        base_config = getattr(new_class, '_etl_config', None)

        if not config:
            config = LoaderOptions(base_config)
        else:
            config = LoaderOptions(config)

        new_class.add_to_class('_etl_config', config)
        new_class.add_to_class('loader', loader)
        #
        # attr_meta = attrs.get('Meta', None)
        # attr_loader = attrs.get('Loader', None)
        # loader = attr_meta or getattr(new_class, 'Meta', None)
        # base_meta = getattr(new_class, '_meta', None)

        return new_class


class DataMartModel(models.Model, metaclass=DataMartModelBase):
    country_name = models.CharField(max_length=100, db_index=True)
    schema_name = models.CharField(max_length=63, db_index=True)
    area_code = models.CharField(max_length=10, db_index=True)
    last_modify_date = models.DateTimeField(blank=True, auto_now=True)
    seen = models.DateTimeField(blank=True, null=True)

    source_id = models.IntegerField(blank=True, null=True)

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
