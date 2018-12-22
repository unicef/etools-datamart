import json

from django.db import models
from django.utils import timezone

from etools_datamart.apps.data.loader import EtlResult, Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import HactAggregatehact


class HACTLoader(Loader):
    def process_country(self, results: EtlResult, country, context):
        today = timezone.now()
        aggregate = HactAggregatehact.objects.get(year=today.year)
        data = json.loads(aggregate.partner_values)

        # # Total number of completed Microassessments in the business area in the past year
        values = dict(microassessments_total=data['assurance_activities']['micro_assessment'],
                      programmaticvisits_total=data['assurance_activities']['programmatic_visits']['completed'],
                      followup_spotcheck=data['assurance_activities']['spot_checks']['follow_up'],
                      completed_spotcheck=data['assurance_activities']['spot_checks']['completed'],
                      completed_hact_audits=data['assurance_activities']['scheduled_audit'],
                      completed_special_audits=data['assurance_activities']['special_audit'],
                      )
        op = self.process(filters=dict(year=today.year,
                                       area_code=country.business_area_code,
                                       country_name=country.name,
                                       schema_name=country.schema_name),
                          values=values)
        results.incr(op)

        return results


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

    loader = HACTLoader()

    class Meta:
        ordering = ('year', 'country_name')
        unique_together = ('year', 'country_name')
        verbose_name = "HACT"
