from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel


class HACT(DataMartModel):
    year = models.IntegerField()
    microassessments_total = models.IntegerField(default=0,
                                                 help_text="Total number of completed Microassessments in the business area in the past year")
    programmaticvisits_total = models.IntegerField(default=0,
                                                   help_text="Total number of completed Programmatic visits in the business area")
    followup_spotcheck = models.IntegerField(default=0,
                                             help_text="Total number of completed Programmatic visits in the business area")
    completed_spotcheck = models.IntegerField(default=0,
                                              help_text="Total number of completed Programmatic visits in the business area")
    completed_hact_audits = models.IntegerField(default=0,
                                                help_text="Total number of completed scheduled audits for the workspace.")
    completed_special_audits = models.IntegerField(default=0,
                                                   help_text="Total number of completed special audits for the workspace. ")
