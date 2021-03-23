import logging

from django.contrib.admin import ModelAdmin, register

from etools_datamart.apps.mart.unpp import models
from etools_datamart.libs.truncate import TruncateTableMixin

logger = logging.getLogger(__name__)


@register(models.Location)
class LocationAdmin(TruncateTableMixin, ModelAdmin):
    list_display = (
        'source_id',
        'name',
        'country_code',
        'latitude',
        'longitude',
    )


@register(models.Application)
class ApplicationAdmin(TruncateTableMixin, ModelAdmin):
    list_display = ('__str__',)
