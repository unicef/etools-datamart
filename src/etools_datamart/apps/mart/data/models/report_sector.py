from django.db import models

from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import ReportsSector


class Section(EtoolsDataMartModel):
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    dashboard = models.BooleanField(null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Options:
        source = ReportsSector
