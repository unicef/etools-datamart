from django.db import models
from django.db.models import F, Q

from etools_datamart.apps.mart.prp.base import PrpDataMartModel
from etools_datamart.apps.mart.prp.models.base import PrpBaseLoader
from etools_datamart.apps.sources.source_prp.models import IndicatorIndicatorlocationdata


class IndicatorByLocationLoader(PrpBaseLoader):
    def get_queryset(self):
        qs = IndicatorIndicatorlocationdata.objects.exclude(
            Q(indicator_report__progress_report__isnull=True)
            | Q(indicator_report__progress_report__status__in=["Due", "Ove", "Sen"])
        ).annotate(
            country=F("indicator_report__progress_report__programme_document__workspace__title"),
            location_source_id=F("location__id"),
            location_name=F("location__name"),
            location_pcode=F("location__p_code"),
            location_level=F("location__admin_level"),
            location_levelname=F("location__admin_level_name"),
            title_of_indicator=F("indicator_report__title"),
            reference_number=F("indicator_report__progress_report__programme_document__reference_number"),
            project=F("indicator_report__project__title"),
            partner=F("indicator_report__project__partner__title"),
            indicator_baseline=F("indicator_report__reportable__baseline"),
            indicator_target=F("indicator_report__reportable__target"),
        )
        return qs


class IndicatorByLocation(PrpDataMartModel):
    country = models.CharField(max_length=100, blank=True, null=True)
    project = models.CharField(max_length=255, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    indicator_target = models.CharField(max_length=50, blank=True, null=True)
    indicator_baseline = models.CharField(max_length=50, blank=True, null=True)
    title_of_indicator = models.TextField(max_length=2048, blank=True, null=True)

    location_source_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=254, blank=True, null=True)
    location_pcode = models.CharField(max_length=32, blank=True, null=True)
    location_level = models.IntegerField(blank=True, null=True)
    location_levelname = models.CharField(max_length=32, blank=True, null=True)

    loader = IndicatorByLocationLoader()

    class Meta:
        app_label = "prp"

    class Options:
        mapping = {}
