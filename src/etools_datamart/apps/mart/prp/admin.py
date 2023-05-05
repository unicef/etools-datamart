import logging

from django.contrib.admin import ModelAdmin, register

from etools_datamart.apps.mart.prp import models
from etools_datamart.libs.truncate import TruncateTableMixin

logger = logging.getLogger(__name__)


@register(models.IndicatorByLocation)
class IndicatorByLocationAdmin(TruncateTableMixin, ModelAdmin):
    list_display = (
        "source_id",
        "project",
        "location_name",
        "country",
        "partner",
        "reference_number",
        "title_of_indicator",
    )
    list_filter = ("country",)
    search_fields = list_display


@register(models.DataReport)
class DataReportAdmin(TruncateTableMixin, ModelAdmin):
    list_display = (
        "current_location",
        "country_name",
        "partner_name",
        "cp_output",
        "intervention_reference_number",
        "report_status",
        "submitted_by",
    )
    list_filter = ("country_name", "partner_name", "cp_output", "report_status")
    search_fields = (
        "current_location",
        "country_name",
        "partner_name",
        "cp_output",
        "intervention_reference_number",
        "report_status",
        "submitted_by",
        "section",
    )


@register(models.IndicatorReport)
class IndicatorReportAdmin(TruncateTableMixin, ModelAdmin):
    list_display = (
        "business_area",
        "pd_output_progress_status",
        "report_type",
        "time_period_start",
        "time_period_end",
        "performance_indicator",
    )
    list_filter = ("business_area", "pd_output_progress_status", "report_type")
    search_fields = ("performance_indicator",)
