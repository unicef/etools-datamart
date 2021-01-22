from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementRiskMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import (
    AuditAudit,
    AuditFinancialfinding,
)

from .partner import Partner


class AuditLoader(EngagementRiskMixin, EtoolsLoader):
    def process_country(self):
        for record in AuditAudit.objects.select_related('engagement_ptr'):
            record.id = record.engagement_ptr_id
            record.sub_type = AuditAudit
            record.engagement_ptr._impl = record
            filters = self.config.key(self, record.engagement_ptr)
            values = self.get_values(record.engagement_ptr)
            op = self.process_record(filters, values)
            self.increment_counter(op)

    def get_financial_findings_count(self, record, values, field_name):
        return AuditFinancialfinding.objects.filter(audit=record._impl).count()

    def get_financial_findings_titles(self, record, values, field_name):
        return list(AuditFinancialfinding.objects.filter(
            audit=record._impl,
        ).values("title").annotate(
            count=Count("title"),
        ).order_by("title"))

    def get_key_internal_control_count(self, record, values, field_name):
        return AuditFinancialfinding.objects.filter(audit=record._impl).count()


class Audit(EtoolsDataMartModel):
    TYPE_AUDIT = 'audit'

    TYPES = Choices(
        (TYPE_AUDIT, _('Audit')),
    )

    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    partner = JSONField(blank=True, null=True, default=dict)
    shared_ip_with = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        verbose_name=_('Shared Audit with'),
    )
    total_value = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=20,
    )
    date_of_final_report = models.DateField(null=True, blank=True)
    audited_expenditure = models.DecimalField(
        verbose_name=_('Audited Expenditure $'),
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=20,
    )
    audited_expenditure_local = models.DecimalField(
        verbose_name=_('Audited Expenditure Local Currency'),
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=20,
    )
    financial_findings = models.DecimalField(
        verbose_name=_('Financial Findings $'),
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=20,
    )
    financial_findings_local = models.DecimalField(
        verbose_name=_('Financial Findings Local Currency'),
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=20,
    )
    audit_opinion = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    financial_findings_count = models.IntegerField(blank=True, null=True)
    financial_findings_titles = JSONField(blank=True, null=True, default=dict)
    key_internal_control_count = models.IntegerField(blank=True, null=True)

    loader = AuditLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditAudit
        sync_deleted_records = lambda a: False
        depends = (Partner, )
        mapping = dict(
            auditor="agreement.auditor_firm.name",
            agreement="agreement.order_number",  # PurchaseOrder
            partner="-",
            financial_findings_count="-",
            financial_findings_titles="-",
            key_internal_control_count="-",
        )
