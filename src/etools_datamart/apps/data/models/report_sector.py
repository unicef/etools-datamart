from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import ReportsSector


class Section(DataMartModel):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    dashboard = models.BooleanField(null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Options:
        source = ReportsSector