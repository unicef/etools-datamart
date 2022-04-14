import logging

from django.contrib.admin import ModelAdmin, register

from etools_datamart.apps.mart.prp import models
from etools_datamart.libs.truncate import TruncateTableMixin

logger = logging.getLogger(__name__)


@register(models.IndicatorByLocation)
class IndicatorByLocationAdmin(TruncateTableMixin, ModelAdmin):
    list_display = ('source_id', 'project', 'location_name',
                    'country', 'partner', 'reference_number', 'title_of_indicator')


@register(models.DataReport)
class DataReportAdmin(TruncateTableMixin, ModelAdmin):
    list_display = ('current_location', 'country_name', 'partner_name', 'cp_output', 'intervention_reference_number', 'pd_result')
    list_filter = ('country_name', 'partner_name', 'cp_output', 'intervention_reference_number')


@register(models.IndicatorReport)
class IndicatorReportAdmin(TruncateTableMixin, ModelAdmin):
    list_display = ('business_area', 'pd_output_progress_status', 'performance_indicator')
    list_filter = ('business_area', 'pd_output_progress_status')
    search_fields = ('performance_indicator', )
