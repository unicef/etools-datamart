from django.db import models

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import PartnersPartnerorganization


class HACTDetailLoader(Loader):
    {'audits': {'completed': 0, 'minimum_requirements': 0},
     'spot_checks': {'completed': {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'total': 0},
                     'follow_up_required': 0},
     'assurance_coverage': 'void',
     'programmatic_visits': {'planned': {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'total': 0},
                             'completed': {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0,
                                           'total': 0}},
     'outstanding_findings': 0}

    def get_values(self, record):
        # data = json.loads(record.hact_values)
        data = record.hact_values
        data[''] = 'N/A'
        ret = super().get_values(record)
        hact_values = dict(ct_1oct_30sep=data[''],
                           expiring_threshold=data[''],
                           approach_threshold=data[''],
                           pv_planned_year=data['programmatic_visits']['planned']['total'],
                           pv_planned_q1=data['programmatic_visits']['planned']['q1'],
                           pv_planned_q2=data['programmatic_visits']['planned']['q2'],
                           pv_planned_q3=data['programmatic_visits']['planned']['q3'],
                           pv_planned_q4=data['programmatic_visits']['planned']['q4'],
                           pv_mr=data[''],
                           pv_completed_year=data['programmatic_visits']['completed']['total'],
                           pv_completed_q1=data['programmatic_visits']['completed']['q1'],
                           pv_completed_q2=data['programmatic_visits']['completed']['q2'],
                           pv_completed_q3=data['programmatic_visits']['completed']['q3'],
                           pv_completed_q4=data['programmatic_visits']['completed']['q4'],
                           sc_planned_year=data[''],
                           sc_planned_q1=data[''],
                           sc_planned_q2=data[''],
                           sc_planned_q3=data[''],
                           sc_planned_q4=data[''],
                           sc_mr=data[''],
                           sc_follow_up=data['spot_checks']['follow_up_required'],
                           sc_completed_year=data['spot_checks']['completed']['total'],
                           sc_completed_q1=data['spot_checks']['completed']['q1'],
                           sc_completed_q2=data['spot_checks']['completed']['q1'],
                           sc_completed_q3=data['spot_checks']['completed']['q1'],
                           sc_completed_q4=data['spot_checks']['completed']['q1'],
                           audits_mr=data['audits']['minimum_requirements'],
                           audits_completed=data['audits']['completed'],
                           audits_outstanding_findings=data['outstanding_findings'], )
        ret.update(hact_values)
        return ret

    def process_country(self):
        for rec in self.get_queryset():
            filters = self.config.key(self, rec)
            values = self.get_values(rec)
            op = self.process_record(filters, values)
            self.increment_counter(op)


class HACTDetail(DataMartModel):
    year = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=300, blank=True, null=True)
    partner_type = models.CharField(max_length=300, blank=True, null=True)
    shared_ip = models.CharField(max_length=300, blank=True, null=True)
    assessment_type = models.CharField(max_length=300, blank=True, null=True)
    ct_1oct_30sep = models.CharField(max_length=300, blank=True, null=True)
    liqu_1oct_30sep = models.CharField(max_length=300, blank=True, null=True)
    ct_jan_dec = models.CharField(max_length=300, blank=True, null=True)
    risk_rating = models.CharField(max_length=300, blank=True, null=True)
    expiring_threshold = models.CharField(max_length=300, blank=True, null=True)
    approach_threshold = models.CharField(max_length=300, blank=True, null=True)
    pv_planned_year = models.CharField(max_length=300, blank=True, null=True)
    pv_planned_q1 = models.CharField(max_length=300, blank=True, null=True)
    pv_planned_q2 = models.CharField(max_length=300, blank=True, null=True)
    pv_planned_q3 = models.CharField(max_length=300, blank=True, null=True)
    pv_planned_q4 = models.CharField(max_length=300, blank=True, null=True)
    pv_mr = models.CharField(max_length=300, blank=True, null=True)
    pv_completed_year = models.CharField(max_length=300, blank=True, null=True)
    pv_completed_q1 = models.CharField(max_length=300, blank=True, null=True)
    pv_completed_q2 = models.CharField(max_length=300, blank=True, null=True)
    pv_completed_q3 = models.CharField(max_length=300, blank=True, null=True)
    pv_completed_q4 = models.CharField(max_length=300, blank=True, null=True)
    sc_planned_year = models.CharField(max_length=300, blank=True, null=True)
    sc_planned_q1 = models.CharField(max_length=300, blank=True, null=True)
    sc_planned_q2 = models.CharField(max_length=300, blank=True, null=True)
    sc_planned_q3 = models.CharField(max_length=300, blank=True, null=True)
    sc_planned_q4 = models.CharField(max_length=300, blank=True, null=True)
    sc_mr = models.CharField(max_length=300, blank=True, null=True)
    sc_follow_up = models.CharField(max_length=300, blank=True, null=True)
    sc_completed_year = models.CharField(max_length=300, blank=True, null=True)
    sc_completed_q1 = models.CharField(max_length=300, blank=True, null=True)
    sc_completed_q2 = models.CharField(max_length=300, blank=True, null=True)
    sc_completed_q3 = models.CharField(max_length=300, blank=True, null=True)
    sc_completed_q4 = models.CharField(max_length=300, blank=True, null=True)
    audits_mr = models.CharField(max_length=300, blank=True, null=True)
    audits_completed = models.CharField(max_length=300, blank=True, null=True)
    audits_outstanding_findings = models.CharField(max_length=300, blank=True, null=True)

    loader = HACTDetailLoader()

    class Meta:
        ordering = ('year', 'country_name')
        unique_together = ('year', 'country_name')
        verbose_name = "HACT Detail"
        verbose_name_plural = "HACT Details"

    class Options:
        source = PartnersPartnerorganization
        sync_deleted_records = lambda loader: False
        truncate = False
        # key = lambda loader, record: dict(country_name=loader.context['country'].name,
        #                                   schema_name=loader.context['country'].schema_name,
        #                                   year=loader.context['today'].year)
        mapping = dict(partner_name='name',
                       partner_type='=',
                       vendor_number='=',
                       shared_ip='=',
                       assessment_type='=',
                       year='N/A',
                       risk_rating='rating',
                       liqu_1oct_30sep='reported_cy',
                       ct_jan_dec='total_ct_ytd',

                       )
