import json

from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import HactHacthistory

{'Implementing Partner': 'ASIAN DISASTER PREPAREDNESS CENTER',
 'Partner Type': 'Civil Society Organization',
 'Shared': 'No',
 'Shared IP': None,
 'TOTAL for current CP cycle': 0.0,
 'PLANNED for current year': 0.0,
 'Current Year (1 Oct - 30 Sep)': 23127.5,
 'Micro Assessment': 'Missing',
 'Risk Rating': 'Non-Assessed',
 'Programmatic Visits Planned': 0,
 'Programmatic Visits M.R': 0,
 'Programmatic Visits Done': 0,
 'Spot Checks M.R': 0,
 'Spot Checks Done': 0,
 'Audits M.R': 0,
 'Audits Done': 0,
 'Flag for Follow up': 0}

# from PartnersPartnerorganization
{'audits': {'completed': 0, 'minimum_requirements': 0},
 'spot_checks': {'completed': {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'total': 0},
                 'follow_up_required': 0},
 'assurance_coverage': 'void',
 'programmatic_visits': {'planned': {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'total': 0},
                         'completed': {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'total': 0}},
 'outstanding_findings': 0}


def get_item(d, target, default: object = 'N/A', sep='|'):
    try:
        parts = target.split(sep)
        for p in parts:
            d = d[p]
        return d
    except KeyError:
        return default


class HACTDetailLoader(EtoolsLoader):

    def get_pv_completed_year(self, record, values, field_name):
        ret = 0
        for i in range(1, 4):
            ret += get_item(self.data1, 'Programmatic Visits Completed Q%s' % i, 0)
        return ret

    def get_pv_planned_year(self, record, values, field_name):
        ret = 0
        for i in range(1, 4):
            ret += get_item(self.data1, 'Programmatic Visits Planned Q%s' % i, 0)
        return ret

    def get_sc_completed_year(self, record, values, field_name):
        ret = 0
        for i in range(1, 4):
            ret += get_item(self.data1, 'Spot Checks Completed Q%s' % i, 0)
        return ret

    def get_sc_planned_year(self, record, values, field_name):
        ret = 0
        for i in range(1, 4):
            ret += get_item(self.data1, 'Spot Checks Planned Q%s' % i, 0) or 0
        return ret

    def get_values(self, record):
        self.data1 = dict(
            json.loads(record.partner_values) if isinstance(record.partner_values, str) else record.partner_values)
        hact_values = dict(
            approach_threshold=get_item(self.data1, 'Approach Threshold', None),
            audits_completed=get_item(self.data1, 'Audit Completed'),
            audits_mr=get_item(self.data1, 'Audits M.R'),
            audits_outstanding_findings=get_item(self.data1, 'Audit Outstanding Findings'),
            ct_1oct_30sep=get_item(self.data1, 'Cash Transfer 1 OCT - 30 SEP'),
            expiring_threshold=get_item(self.data1, 'Expiring Threshold', None),
            pv_completed_q1=get_item(self.data1, 'Programmatic Visits Completed Q1'),
            pv_completed_q2=get_item(self.data1, 'Programmatic Visits Completed Q2'),
            pv_completed_q3=get_item(self.data1, 'Programmatic Visits Completed Q3'),
            pv_completed_q4=get_item(self.data1, 'Programmatic Visits Completed Q4'),
            # pv_completed_year=get_item(data, 'programmatic_visits|completed|total'),
            pv_mr=get_item(self.data1, 'Programmatic Visits M.R'),
            pv_planned_q1=get_item(self.data1, 'Programmatic Visits Planned Q1'),
            pv_planned_q2=get_item(self.data1, 'Programmatic Visits Planned Q2'),
            pv_planned_q3=get_item(self.data1, 'Programmatic Visits Planned Q3'),
            pv_planned_q4=get_item(self.data1, 'Programmatic Visits Planned Q4'),
            # pv_planned_year=get_item(data, 'programmatic_visits|planned|total'),
            sc_completed_q1=get_item(self.data1, 'Spot Checks Completed Q1'),
            sc_completed_q2=get_item(self.data1, 'Spot Checks Completed Q2'),
            sc_completed_q3=get_item(self.data1, 'Spot Checks Completed Q3'),
            sc_completed_q4=get_item(self.data1, 'Spot Checks Completed Q4'),
            # sc_completed_year=get_item(data, 'spot_checks|completed|total'),
            sc_follow_up=get_item(self.data1, 'Flag for Follow up', None),
            sc_mr=get_item(self.data1, 'Spot Checks M.R'),
            sc_planned_q1=get_item(self.data1, 'Spot Checks Planned Q1'),
            sc_planned_q2=get_item(self.data1, 'Spot Checks Planned Q2'),
            sc_planned_q3=get_item(self.data1, 'Spot Checks Planned Q3'),
            sc_planned_q4=get_item(self.data1, 'Spot Checks Planned Q4'),
            # sc_planned_year=get_item(self.data1, ''),
            shared_ip=get_item(self.data1, 'Shared IP'),
        )
        self.mapping.update(hact_values)
        ret = super().get_values(record)
        ret.update(hact_values)
        return ret

    def process_country(self):
        for rec in self.get_queryset():
            filters = self.config.key(self, rec)
            values = self.get_values(rec)
            op = self.process_record(filters, values)
            self.increment_counter(op)


class HACTHistory(EtoolsDataMartModel):
    year = models.IntegerField(blank=True, null=True, db_index=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    partner_source_id = models.IntegerField(blank=True, null=True)
    vendor_number = models.CharField(max_length=300, blank=True, null=True)
    partner_type = models.CharField(max_length=300, blank=True, null=True)
    shared_ip = models.CharField(max_length=300, blank=True, null=True)
    assessment_type = models.CharField(max_length=300, blank=True, null=True, db_index=True)
    ct_1oct_30sep = models.CharField(max_length=300, blank=True, null=True)
    liqu_1oct_30sep = models.CharField(max_length=300, blank=True, null=True)
    ct_jan_dec = models.CharField(max_length=300, blank=True, null=True)
    risk_rating = models.CharField(max_length=300, blank=True, null=True)
    expiring_threshold = models.BooleanField(blank=True, null=True)
    approach_threshold = models.BooleanField(blank=True, null=True)
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
    sc_follow_up = models.BooleanField(blank=True, null=True)
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
        verbose_name = "HACT Detail"
        verbose_name_plural = "HACT Details"
        unique_together = (('partner_source_id', 'year', 'country_name'),)

    class Options:
        source = HactHacthistory
        queryset = HactHacthistory.objects.select_related('partner').all
        sync_deleted_records = lambda loader: False
        truncate = True
        # key = lambda loader, record: dict(country_name=loader.context['country'].name,
        #                                   schema_name=loader.context['country'].schema_name,
        #                                   year=loader.context['today'].year)
        mapping = dict(partner_name='partner.name',
                       partner_type='partner.partner_type',
                       vendor_number='partner.vendor_number',
                       partner_source_id='partner.id',
                       shared_ip='N/A',
                       assessment_type='partner.type_of_assessment',
                       year='year',
                       risk_rating='partner.rating',
                       liqu_1oct_30sep='partner.reported_cy',
                       ct_jan_dec='partner.total_ct_ytd',
                       )
