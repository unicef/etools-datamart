import json

from django.db import models

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import HactAggregatehact


class HACTLoader(Loader):

    def get_queryset(self):
        return HactAggregatehact.objects.filter(year=self.context['today'].year)

    def process_country(self):
        country = self.context['country']
        try:
            aggregate = self.get_queryset().get()

            data = json.loads(aggregate.partner_values)

            # # Total number of completed Microassessments in the business area in the past year
            values = dict(microassessments_total=data['assurance_activities']['micro_assessment'],
                          programmaticvisits_total=data['assurance_activities']['programmatic_visits']['completed'],
                          followup_spotcheck=data['assurance_activities']['spot_checks']['follow_up'],
                          completed_spotcheck=data['assurance_activities']['spot_checks']['completed'],
                          completed_hact_audits=data['assurance_activities']['scheduled_audit'],
                          completed_special_audits=data['assurance_activities']['special_audit'],
                          seen=self.context['today'])
            op = self.process_record(filters=dict(year=self.context['today'].year,
                                                  area_code=country.business_area_code,
                                                  country_name=country.name,
                                                  schema_name=country.schema_name),
                                     values=values)
            self.increment_counter(op)
        except HactAggregatehact.DoesNotExist:  # pragma: no cover
            pass


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

    class Option:
        truncate = True
