from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import AuditDetailedfindinginfo, AuditEngagement, AuditMicroassessment

from .partner import Partner


class MicroAssessmentLoader(EngagementMixin, EtoolsLoader):
    def process_country(self):
        for record in AuditMicroassessment.objects.select_related('engagement_ptr'):
            record.id = record.engagement_ptr_id
            record.sub_type = AuditMicroassessment
            record.engagement_ptr._impl = record
            filters = self.config.key(self, record.engagement_ptr)
            values = self.get_values(record.engagement_ptr)
            op = self.process_record(filters, values)
            self.increment_counter(op)

    def get_subject_area(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {'blueprint__category__code': "ma_subject_areas"}
        value, count = self._get_risks(record, **filters)
        return value

    def get_test_subject_areas(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {'blueprint__category__code': "test_subject_areas"}
        value, count = self._get_risks(record, **filters)
        values["test_subject_areas_count"] = count
        return value

    def get_findings_count(self, record: AuditEngagement, values: dict, **kwargs):
        return AuditDetailedfindinginfo.objects.filter(micro_assesment__pk=record.pk).count()

    def risk_rating_helper(self, record: AuditEngagement, header):
        filters = {'blueprint__category__code': "ma_subject_areas", 'blueprint__header': header}
        value, extra, text = self._get_risk(record, **filters)
        return text

    def get_overall_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {'blueprint__category__code': "ma_global_assessment"}
        value, extra, text = self._get_risk(record, **filters)
        return text

    def get_implementing_partner_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Implementing partner")

    def get_programme_management_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Programme Management")

    def get_organizational_structure_and_staffing_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Organizational structure and staffing")

    def get_accounting_policies_and_procedures_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Accounting policies and procedures")

    def get_fixed_assets_and_inventory_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Fixed Assets and Inventory")

    def get_financial_reporting_and_monitoring_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Financial Reporting and Monitoring")

    def get_procurement_and_contract_administration_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        return self.risk_rating_helper(record, "Procurement")


class MicroAssessment(EtoolsDataMartModel):
    TYPE_MICRO_ASSESSMENT = 'ma'

    TYPES = Choices(
        (TYPE_MICRO_ASSESSMENT, _('Micro Assessment')),
    )

    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    status = models.CharField(max_length=30, blank=True, null=True,
                              choices=AuditEngagementConsts.DISPLAY_STATUSES,
                              db_index=True)
    created = models.DateField(blank=True, null=True)

    # Engagement Overview
    partner = JSONField(blank=True, null=True, default=dict)
    agreement = models.CharField(max_length=300, blank=True, null=True)
    shared_ip_with = ArrayField(models.CharField(max_length=20, blank=True, null=True),
        blank=True, null=True, default=list, verbose_name=_('Shared Audit with'))

    # Report Section
    # sections = models.TextField(blank=True, null=True)
    # sections_data = JSONField(blank=True, null=True, default=dict)
    # offices = models.TextField(blank=True, null=True)
    # offices_data = JSONField(blank=True, null=True, default=dict)
    date_of_field_visit = models.DateField(null=True, blank=True)
    date_of_final_report = models.DateField(null=True, blank=True)

    rating = models.CharField(max_length=50, blank=True, null=True)
    rating_extra = JSONField(blank=True, null=True, default=dict)
    subject_area = models.TextField(blank=True, null=True)
    subject_area_extra = JSONField(blank=True, null=True, default=dict)
    test_subject_areas = models.TextField(blank=True, null=True)
    test_subject_areas_count = models.IntegerField(blank=True, null=True)

    # Detailed Findings
    findings_count = models.IntegerField(blank=True, null=True)

    # Questionnaire Section
    overall_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    implementing_partner_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    programme_management_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    organizational_structure_and_staffing_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    accounting_policies_and_procedures_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    fixed_assets_and_inventory_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    financial_reporting_and_monitoring_risk_rating = models.CharField(max_length=16, blank=True, null=True)
    procurement_and_contract_administration_risk_rating = models.CharField(max_length=16, blank=True, null=True)

    # Action Points
    action_points = JSONField(blank=True, null=True, default=dict)
    action_points_data = JSONField(blank=True, null=True, default=dict)

    loader = MicroAssessmentLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditMicroassessment
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            agreement="agreement.order_number",  # PurchaseOrder
            partner="-",
            rating="-",
            rating_extra="i",
            subject_area="-",
            subject_area_extra="i",
            test_subject_areas="-",
            test_subject_areas_count='i',
            implementing_partner_risk_rating='-',
            findings_count='-',
            overall_risk_rating='-',
            programme_management_risk_rating='-',
            organizational_structure_and_staffing_risk_rating='-',
            accounting_policies_and_procedures_risk_rating='-',
            fixed_assets_and_inventory_risk_rating='-',
            financial_reporting_and_monitoring_risk_rating='-',
            procurement_and_contract_administration_risk_rating='-',
            action_points='-',
            action_points_data='i',
        )
