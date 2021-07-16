from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import ReportsResult


class Result(EtoolsDataMartModel):
    name = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    result_type = models.CharField(max_length=150, blank=True, null=True)
    section = models.CharField(max_length=128, blank=True, null=True)
    gic_code = models.CharField(max_length=8, blank=True, null=True)
    gic_name = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_tag = models.BooleanField(blank=True, null=True)
    sic_code = models.CharField(max_length=8, blank=True, null=True)
    sic_name = models.CharField(max_length=255, blank=True, null=True)
    wbs = models.CharField(max_length=50, blank=True, null=True)
    activity_focus_code = models.CharField(max_length=8, blank=True, null=True)
    activity_focus_name = models.CharField(max_length=255, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    ram = models.BooleanField(blank=True, null=True)
    country_programme = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_marker_code = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_marker_name = models.CharField(max_length=255, blank=True, null=True)
    programme_area_code = models.CharField(max_length=16, null=True, blank=True)
    programme_area_name = models.CharField(max_length=255, null=True, blank=True)

    loader = EtoolsLoader()

    class Options:
        source = ReportsResult
        mapping = dict(
            result_type="result_type.name",
            section="sector.name",
            country_programme="country_programme.name",
        )
