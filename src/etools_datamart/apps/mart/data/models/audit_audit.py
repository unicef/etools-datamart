from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Count, JSONField, Sum
from django.utils.translation import gettext as _

from _decimal import DivisionByZero, InvalidOperation
from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import AuditAudit, AuditFinancialfinding, AuditKeyinternalcontrol

from .partner import Partner


class AuditLoader(EngagementMixin, EtoolsLoader):
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
        qs = AuditFinancialfinding.objects.filter(audit=record._impl)
        values["financial_findings_amount"] = 0 or qs.aggregate(Sum('amount'))['amount__sum']
        try:
            perc = 100 * record._impl.financial_findings / record._impl.audited_expenditure
        except (TypeError, DivisionByZero, InvalidOperation):
            perc = 0
        values['percent_of_audited_expenditure'] = perc
        values['pending_unsupported_amount'] = record._impl.financial_findings - record.amount_refunded \
            - record.additional_supporting_documentation_provided \
            - record.justification_provided_and_accepted - record.write_off_required

        return qs.count()

    def get_financial_findings_by_category(self, record, values, field_name):
        return []

    def get_key_internal_control_count(self, record, values, field_name):
        return AuditKeyinternalcontrol.objects.filter(audit=record._impl).count()

    def get_key_internal_control_by_category(self, record, values, field_name):
        return []


class Audit(EtoolsDataMartModel):
    created = models.DateField(blank=True, null=True)
    TYPE_AUDIT = 'audit'

    TYPES = Choices(
        (TYPE_AUDIT, _('Audit')),
    )

    reference_number = models.CharField(max_length=100, blank=True, null=True)
    engagement_type = models.CharField(max_length=300, blank=True, null=True, choices=TYPES, db_index=True)
    status = models.CharField(max_length=30, blank=True, null=True,
                              choices=AuditEngagementConsts.DISPLAY_STATUSES,
                              db_index=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # Engagement Overview Card
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    partner = JSONField(blank=True, null=True, default=dict)
    shared_ip_with = ArrayField(models.CharField(max_length=20, blank=True, null=True),
                                blank=True, null=True, default=list, verbose_name=_('Shared Audit with'))
    total_value = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)
    date_of_final_report = models.DateField(null=True, blank=True)

    # Audit - Report Section
    audited_expenditure = models.DecimalField(
        verbose_name=_('Audited Expenditure $'), blank=True, null=True, decimal_places=2, max_digits=20)
    audited_expenditure_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    financial_findings_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    audit_opinion = models.CharField(max_length=254, blank=True, null=True)
    justification_provided_and_accepted = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    write_off_required = models.DecimalField('Impairment', max_digits=20, decimal_places=2, blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    pending_unsupported_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    percent_of_audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    test_subject_areas_count = models.IntegerField(blank=True, null=True)

    financial_findings = models.DecimalField(
        verbose_name=_('Financial Findings $'), blank=True, null=True, decimal_places=2, max_digits=20)
    financial_findings_by_category = JSONField(blank=True, null=True, default=dict)
    financial_findings_count = models.IntegerField(blank=True, null=True)
    financial_findings_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    key_internal_control_by_category = JSONField(blank=True, null=True, default=dict)
    key_internal_control_count = models.IntegerField(blank=True, null=True)

    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)

    # Action Points
    action_points = JSONField(blank=True, null=True, default=dict)
    action_points_data = JSONField(blank=True, null=True, default=dict)

    loader = AuditLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditAudit
        sync_deleted_records = lambda a: False
        depends = (Partner, )
        mapping = dict(
            auditor="agreement.auditor_firm.name",
            auditor_number="agreement.auditor_firm.vendor_number",
            agreement="agreement.order_number",  # PurchaseOrder
            start_date='_impl.start_date',
            end_date='_impl.end_date',
            financial_findings='_impl.financial_findings',
            audit_opinion='_impl.audit_opinion',
            audited_expenditure='_impl.audited_expenditure',
            partner="-",
            financial_findings_count="-",
            key_internal_control_count="-",
            financial_findings_amount="i",
            percent_of_audited_expenditure="i",
            pending_unsupported_amount='i',
            test_subject_areas_count='i',
            action_points='-',
            action_points_data='i',
            key_internal_control_by_category='-',
            financial_findings_by_category='-'
        )
