from django.db import models

from etools_datamart.apps.core.models import DataMartManager
from etools_datamart.apps.mart.data.loader import CommonSchemaLoader
from etools_datamart.apps.mart.data.models.base import CommonDataMartModel
from etools_datamart.apps.sources.etools.models import UsersCountry


class Workspace(CommonDataMartModel):
    schema_name = models.CharField(max_length=63)
    name = models.CharField(max_length=100)
    business_area_code = models.CharField(max_length=10)
    initial_zoom = models.IntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    country_short_code = models.CharField(max_length=10)
    vision_sync_enabled = models.BooleanField()
    vision_last_synced = models.DateTimeField(blank=True, null=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    currency_name = models.CharField(max_length=128, blank=True, null=True)

    long_name = models.CharField(max_length=255)
    iso3_code = models.CharField(max_length=3, blank=True, null=True)
    custom_dashboards = models.JSONField(blank=True, null=True)

    objects = DataMartManager()
    loader = CommonSchemaLoader()

    class Meta:
        ordering = ("name",)

    class Options:
        source = UsersCountry
        sync_deleted_records = lambda loader: False
        truncate = True
        key = lambda loader, record: dict(source_id=record.id)
        queryset = lambda: UsersCountry.objects.select_related("local_currency")
        mapping = dict(
            currency_code="local_currency.code", currency_name="local_currency.name", schema_name="schema_name"
        )
