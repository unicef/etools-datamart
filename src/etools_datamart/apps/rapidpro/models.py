from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

from celery.local import class_property
from constance import config

from etools_datamart.apps.data.models.base import DataMartManager
from etools_datamart.apps.etl.base import DataMartModelBase
from etools_datamart.apps.rapidpro.loader import TembaLoader, TembaLoaderOptions


class RapidProModelBase(DataMartModelBase):
    loader_option_class = TembaLoaderOptions
    loader_class = TembaLoader


class Source(models.Model):
    name = models.CharField(max_length=100)
    api_token = models.CharField(max_length=40)
    server = models.CharField(max_length=100, default=config.RAPIDPRO_ADDRESS)
    is_active = models.BooleanField(default=False)

    class Meta:
        app_label = 'rapidpro'


class Organization(models.Model):
    {
        "uuid": "6a44ca78-a4c2-4862-a7d3-2932f9b3a7c3",
        "name": "Nyaruka",
        "country": "RW",
        "languages": ["eng", "fra"],
        "primary_language": "eng",
        "timezone": "Africa/Kigali",
        "date_style": "day_first",
        "credits": {"used": 121433, "remaining": 3452},
        "anon": False
    }
    source = models.OneToOneField(Source, on_delete=models.CASCADE,
                                  blank=True, null=True)
    # uuid = models.UUIDField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    primary_language = models.CharField(max_length=100, null=True, blank=True)
    languages = ArrayField(models.CharField(max_length=100))
    timezone = models.CharField(max_length=100, null=True, blank=True)
    date_style = models.CharField(max_length=100, null=True, blank=True)
    credits = JSONField(default=dict)
    anon = models.BooleanField(default=False)

    objects = DataMartManager()

    # loader = TembaLoader()
    class Meta:
        app_label = 'rapidpro'

    class Options:
        source = 'https://app.rapidpro.io/api/v2/org'

    def __str__(self):
        return self.name


class RapidProManager(DataMartManager):
    pass


class RapidProDataMartModel(models.Model, metaclass=RapidProModelBase):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    objects = RapidProManager()

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


class Group(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True)
    name = models.TextField()
    query = models.TextField(null=True, blank=True)
    count = models.IntegerField()
    status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization)

    class Options:
        source = 'groups'
