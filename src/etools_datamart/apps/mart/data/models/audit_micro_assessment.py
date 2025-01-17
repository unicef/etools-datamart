from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.paginator import Paginator
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext as _

from celery.utils.log import get_task_logger
from model_utils import Choices

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import AuditDetailedfindinginfo, AuditEngagement, AuditMicroassessment

from .partner import Partner

logger = get_task_logger(__name__)


class MicroAssessmentLoader(EngagementMixin, EtoolsLoader):
    """
    --
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "audit_microassessment";

    --
    SELECT '##COUNTRY##' AS __schema,
           "audit_microassessment"."engagement_ptr_id",
           "audit_microassessment"."questionnaire_version",

           "audit_engagement"."id",
           "audit_engagement"."created",
           "audit_engagement"."modified",
           "audit_engagement"."status",
           "audit_engagement"."partner_contacted_at",
           "audit_engagement"."engagement_type",
           "audit_engagement"."start_date",
           "audit_engagement"."end_date",
           "audit_engagement"."total_value",
           "audit_engagement"."date_of_field_visit",
           "audit_engagement"."date_of_draft_report_to_ip",
           "audit_engagement"."date_of_comments_by_ip",
           "audit_engagement"."date_of_draft_report_to_unicef",
           "audit_engagement"."date_of_comments_by_unicef",
           "audit_engagement"."date_of_report_submit",
           "audit_engagement"."date_of_final_report",
           "audit_engagement"."date_of_cancel",
           "audit_engagement"."amount_refunded",
           "audit_engagement"."additional_supporting_documentation_provided",
           "audit_engagement"."justification_provided_and_accepted",
           "audit_engagement"."write_off_required",
           "audit_engagement"."cancel_comment",
           "audit_engagement"."explanation_for_additional_information",
           "audit_engagement"."partner_id",
           "audit_engagement"."joint_audit",
           "audit_engagement"."agreement_id",
           "audit_engagement"."po_item_id",
           "audit_engagement"."shared_ip_with",
           "audit_engagement"."exchange_rate",
           "audit_engagement"."currency_of_report",
           "audit_engagement"."reference_number",
           "audit_engagement"."year_of_audit"
    FROM "audit_microassessment"
    INNER JOIN "audit_engagement" ON ("audit_microassessment"."engagement_ptr_id" = "audit_engagement"."id")
    ORDER BY "audit_microassessment"."engagement_ptr_id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;


    -- Partner organization records for audit_engagement records
    SELECT '##COUNTRY##' AS __schema,
           "partners_partnerorganization"."id",
           "partners_partnerorganization"."description",
           "partners_partnerorganization"."address",
           "partners_partnerorganization"."email",
           "partners_partnerorganization"."phone_number",
           "partners_partnerorganization"."alternate_id",
           "partners_partnerorganization"."alternate_name",
           "partners_partnerorganization"."rating",
           "partners_partnerorganization"."core_values_assessment_date",
           "partners_partnerorganization"."vision_synced",
           "partners_partnerorganization"."type_of_assessment",
           "partners_partnerorganization"."last_assessment_date",
           "partners_partnerorganization"."hidden",
           "partners_partnerorganization"."deleted_flag",
           "partners_partnerorganization"."total_ct_cp",
           "partners_partnerorganization"."total_ct_cy",
           "partners_partnerorganization"."blocked",
           "partners_partnerorganization"."city",
           "partners_partnerorganization"."country",
           "partners_partnerorganization"."postal_code",
           "partners_partnerorganization"."shared_with",
           "partners_partnerorganization"."street_address",
           "partners_partnerorganization"."hact_values",
           "partners_partnerorganization"."created",
           "partners_partnerorganization"."modified",
           "partners_partnerorganization"."net_ct_cy",
           "partners_partnerorganization"."reported_cy",
           "partners_partnerorganization"."total_ct_ytd",
           "partners_partnerorganization"."basis_for_risk_rating",
           "partners_partnerorganization"."manually_blocked",
           "partners_partnerorganization"."outstanding_dct_amount_6_to_9_months_usd",
           "partners_partnerorganization"."outstanding_dct_amount_more_than_9_months_usd",
           "partners_partnerorganization"."highest_risk_rating_name",
           "partners_partnerorganization"."highest_risk_rating_type",
           "partners_partnerorganization"."psea_assessment_date",
           "partners_partnerorganization"."sea_risk_rating_name",
           "partners_partnerorganization"."lead_office_id",
           "partners_partnerorganization"."lead_section_id",
           "partners_partnerorganization"."organization_id"

           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id"
    FROM "partners_partnerorganization"
        INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id"="organizations_organization"."id")
    WHERE "partners_partnerorganization"."id" IN (##LIST OF "audit_engagement"."partner_id" IN THE PAGE## )

    --
    SELECT "purchase_order_purchaseorder"."id",
           "purchase_order_purchaseorder"."created",
           "purchase_order_purchaseorder"."modified",
           "purchase_order_purchaseorder"."order_number",
           "purchase_order_purchaseorder"."contract_start_date",
           "purchase_order_purchaseorder"."contract_end_date",
           "purchase_order_purchaseorder"."auditor_firm_id",

           "purchase_order_auditorfirm"."created",
           "purchase_order_auditorfirm"."modified",
           "purchase_order_auditorfirm"."street_address",
           "purchase_order_auditorfirm"."city",
           "purchase_order_auditorfirm"."postal_code",
           "purchase_order_auditorfirm"."country",
           "purchase_order_auditorfirm"."email",
           "purchase_order_auditorfirm"."phone_number",
           "purchase_order_auditorfirm"."blocked",
           "purchase_order_auditorfirm"."hidden",
           "purchase_order_auditorfirm"."deleted_flag",
           "purchase_order_auditorfirm"."vision_synced",
           "purchase_order_auditorfirm"."unicef_users_allowed",
           "purchase_order_auditorfirm"."organization_id"
    FROM "purchase_order_purchaseorder"
    INNER JOIN  "purchase_order_auditorfirm" ON ("purchase_order_purchaseorder"."auditor_firm_id"="purchase_order_auditorfirm"."id")
    WHERE "purchase_order_purchaseorder"."id" IN (## LIST OF "audit_engagement"."agreement_id"## IN THE PAGE##);


    SELECT 'afghanistan' AS __schema,
           "audit_risk"."id",
           "audit_risk"."value",
           "audit_risk"."extra",
           "audit_risk"."blueprint_id",
           "audit_risk"."engagement_id"
    FROM "audit_risk"
    INNER JOIN "audit_riskblueprint" ON ("audit_risk"."blueprint_id" = "audit_riskblueprint"."id")
    INNER JOIN "audit_riskcategory" ON ("audit_riskblueprint"."category_id" = "audit_riskcategory"."id") WHERE ("audit_riskcategory"."code" = 'ma_global_assessment'
          AND "audit_risk"."engagement_id" IN (## LIST OF "audit_microassessment"."engagement_ptr_id" in the PAGE##)));


    SELECT '##COUNTRY##' AS __schema,
           "audit_riskblueprint"."id",
           "audit_riskblueprint"."order",
           "audit_riskblueprint"."weight",
           "audit_riskblueprint"."is_key",
           "audit_riskblueprint"."header",
           "audit_riskblueprint"."description",
           "audit_riskblueprint"."category_id"
    FROM "audit_riskblueprint"
    WHERE "audit_riskblueprint"."id" IN( ##LIST OF "audit_risk"."blueprint_id" IN THE PAGE##)



    """

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = AuditMicroassessment.objects.select_related("engagement_ptr")

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                record.id = record.engagement_ptr_id
                record.sub_type = AuditMicroassessment
                record.engagement_ptr._impl = record
                filters = self.config.key(self, record.engagement_ptr)
                values = self.get_values(record.engagement_ptr)
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def get_subject_area(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {"blueprint__category__code": "ma_subject_areas"}
        value, count = self._get_risks(record, **filters)
        return value

    def get_test_subject_areas(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {"blueprint__category__code": "test_subject_areas"}
        value, count = self._get_risks(record, **filters)
        values["test_subject_areas_count"] = count
        return value

    def get_findings_count(self, record: AuditEngagement, values: dict, **kwargs):
        return AuditDetailedfindinginfo.objects.filter(micro_assesment__pk=record.pk).count()

    def risk_rating_helper(self, record: AuditEngagement, header):
        filters = {"blueprint__category__code": "ma_subject_areas", "blueprint__header": header}
        value, extra, text = self._get_risk(record, **filters)
        return text

    def get_overall_risk_rating(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {"blueprint__category__code": "ma_global_assessment"}
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
    TYPE_MICRO_ASSESSMENT = "ma"

    TYPES = Choices(
        (TYPE_MICRO_ASSESSMENT, _("Micro Assessment")),
    )
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )
    created = models.DateField(blank=True, null=True)

    # Engagement Overview
    partner = JSONField(blank=True, null=True, default=dict)
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    shared_ip_with = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        verbose_name=_("Shared Audit with"),
    )

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
            auditor="agreement.auditor_firm.organization.name",
            auditor_number="agreement.auditor_firm.organization.vendor_number",
            partner="-",
            rating="-",
            rating_extra="i",
            subject_area="-",
            subject_area_extra="i",
            test_subject_areas="-",
            test_subject_areas_count="i",
            implementing_partner_risk_rating="-",
            findings_count="-",
            overall_risk_rating="-",
            programme_management_risk_rating="-",
            organizational_structure_and_staffing_risk_rating="-",
            accounting_policies_and_procedures_risk_rating="-",
            fixed_assets_and_inventory_risk_rating="-",
            financial_reporting_and_monitoring_risk_rating="-",
            procurement_and_contract_administration_risk_rating="-",
            action_points="-",
            action_points_data="i",
        )
