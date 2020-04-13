from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import (AuditAudit, AuditFinancialfinding,
                                                        AuditKeyinternalcontrol, AuditRisk,)


class AuditResultLoader(EtoolsLoader):

    def get_mart_values(self, record: AuditAudit = None):
        ret = super().get_mart_values(None)
        ret['source_id'] = record.engagement_ptr_id
        return ret

    def get_queryset(self):
        return super().get_queryset()

    def get_count_high_risk_findings(self, record, values, field_name):
        return AuditRisk.objects.filter(value=4, engagement=record.engagement_ptr).count()

    def get_count_financial_findings(self, record, values, field_name):
        # count(Audit.FinancialFinding) per engagement.
        return AuditFinancialfinding.objects.filter(audit=record).count()

    def get_count_key_control_weaknesses(self, record, values, field_name):
        return AuditKeyinternalcontrol.objects.filter(audit=record).count()


class AuditResult(EtoolsDataMartModel):
    # Implementing_Business_Area schema - -

    # AuditAudit.engagement_ptr.agreement.auditor_firm.name - -
    vendor = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=300, blank=True, null=True)

    # AuditAudit.engagement_ptr.partner.partner_type - -
    partner_type = models.CharField(max_length=300, blank=True, null=True)

    # AuditAudit.engagement_ptr.partner.rating
    risk_rating = models.CharField(max_length=50, blank=True, null=True)

    # AuditAudit.audited_expenditure
    audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2)

    # AuditAudit.financial_findings - -
    financial_findings = models.DecimalField(max_digits=20, decimal_places=2)

    # AuditAudit.audit_opinion - -
    audit_opinion = models.CharField(max_length=20)

    #  AuditAudit.engagement_ptr.filter(AuditRisk_engagement=4)
    count_high_risk_findings = models.IntegerField(blank=True, null=True)

    #  model count(Audit.FinancialFinding) per engagement.
    count_financial_findings = models.IntegerField(blank=True, null=True)

    # model count(Audit.KeyInternalControl) per engagement
    count_key_control_weaknesses = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=30, blank=True, null=True,
                              choices=AuditEngagementConsts.DISPLAY_STATUSES,
                              db_index=True)

    loader = AuditResultLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditAudit
        sync_deleted_records = lambda loader: False
        mapping = {'source_id': 'engagement_ptr.id',
                   'vendor': 'engagement_ptr.partner.name',
                   'status': 'engagement_ptr.status',
                   'vendor_number': 'engagement_ptr.partner.vendor_number',
                   'partner_type': 'engagement_ptr.partner.partner_type',
                   'risk_rating': 'engagement_ptr.partner.rating',
                   'audited_expenditure': '=',
                   'financial_findings': '=',
                   'audit_opinion': '=',
                   'count_high_risk_findings': '-',
                   'count_financial_findings': '-',
                   'count_key_control_weaknesses': '-',

                   }
