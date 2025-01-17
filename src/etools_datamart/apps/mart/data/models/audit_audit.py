from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.paginator import Paginator
from django.db import models
from django.db.models import JSONField, Sum
from django.utils.translation import gettext as _

from _decimal import DivisionByZero, InvalidOperation
from celery.utils.log import get_task_logger
from model_utils import Choices

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import AuditAudit, AuditFinancialfinding, AuditKeyinternalcontrol

from .partner import Partner

logger = get_task_logger(__name__)


class AuditLoader(EngagementMixin, EtoolsLoader):
    """
    -- Set country schema
    SET search_path = public, ##COUNTRY##;

    -- Count for paging;
    SELECT COUNT(*) AS "__count" FROM "audit_audit";

    -- Audit
    SELECT '##COUNTRY##' AS __schema,
           "audit_audit"."engagement_ptr_id",
           "audit_audit"."audited_expenditure",
           "audit_audit"."financial_findings",
           "audit_audit"."audit_opinion",
           "audit_audit"."audited_expenditure_local",
           "audit_audit"."financial_findings_local",

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
           "audit_engagement"."year_of_audit",

           "purchase_order_purchaseorder"."id",
           "purchase_order_purchaseorder"."created",
           "purchase_order_purchaseorder"."modified",
           "purchase_order_purchaseorder"."order_number",
           "purchase_order_purchaseorder"."contract_start_date",
           "purchase_order_purchaseorder"."contract_end_date",
           "purchase_order_purchaseorder"."auditor_firm_id",
           "purchase_order_auditorfirm"."id",
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
           "purchase_order_auditorfirm"."organization_id",

           "organizations_organization"."id",
           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id",

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
           --"partners_partnerorganiazation"."sea_risk_rating_name",
           "partners_partnerorganization"."lead_office_id",
           "partners_partnerorganization"."lead_section_id",
           "partners_partnerorganization"."organization_id"

    FROM "audit_audit"
    INNER JOIN "audit_engagement" ON ("audit_audit"."engagement_ptr_id" = "audit_engagement"."id")
    INNER JOIN "purchase_order_purchaseorder" ON ("audit_engagement"."agreement_id" = "purchase_order_purchaseorder"."id")
    INNER JOIN "purchase_order_auditorfirm" ON ("purchase_order_purchaseorder"."auditor_firm_id" = "purchase_order_auditorfirm"."id")
    INNER JOIN "organizations_organization" ON ("purchase_order_auditorfirm"."organization_id" = "organizations_organization"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_partnerorganization"."id" = audit_engagement"."partner_id")
    ORDER BY "audit_audit"."engagement_ptr_id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --Audit Engagement Sections
    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_sections"."id",
           "audit_engagement_sections"."engagement_id",
           "audit_engagement_sections"."section_id"
    FROM  "audit_engagement_sections"
    WHERE "audit_engagement_sections"."engagement_id" in  (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##);

    --Audit Engagement Offices
    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_offices"."id",
           "audit_engagement_offices"."engagement_id",
           "audit_engagement_offices"."office_id"
    FROM   "audit_engagement_offices"
    WHERE "audit_engagement_sections"."engagement_id" in  (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##);


    --Audit Financial Findings: Summing can be left to (T)ransform stage
    SELECT "audit_financialfinding"."audit_id",
            SUM("audit_financialfinding"."amount") as amount_sum
    FROM "audit_financialfinding"
    WHERE "audit_financialfinding"."audit_id" in (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY "audit_financialfinding"."audit_id"
    ORDER BY "audit_financialfinding"."audit_id" ASC;

    --Audit Key Internal Count per audit_id
    SELECT audit_id,
           COUNT(*) AS "__count"
    FROM "audit_keyinternalcontrol"
    WHERE "audit_keyinternalcontrol"."audit_id" in (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY audit_id
    ORDER BY audit_id ASC;

    -- Action Point Status Counts: Counting can be left to (T)ransform stage
    SELECT "engagement_id",
           "action_points_actionpoint"."status",
           COUNT("action_points_actionpoint"."status") AS "count"
    FROM "action_points_actionpoint"
    WHERE "action_points_actionpoint"."engagement_id" in (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY "action_points_actionpoint"."engagement_id"
    ORDER BY "action_points_actionpoint"."status" ASC;

    -- Action Point High Priority count per engagement_id : Counting can be left to (T)ransform stage
    SELECT "action_points_actionpoint"."engagement_id"
           "action_points_actionpoint"."high_priority",
           COUNT("action_points_actionpoint"."high_priority") AS "count"
    FROM "action_points_actionpoint"
    WHERE "action_points_actionpoint"."engagement_id" in (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY "action_points_actionpoint"."engagement_id","action_points_actionpoint"."high_priority"
    ORDER BY "action_points_actionpoint"."engagement_id","action_points_actionpoint"."high_priority" ASC

    -- Count description per engagement_id : Counting can be left to (T)ransform stage
    SELECT "categories_category"."description",
           "action_points_actionpoint"."engagement_id",
           COUNT("categories_category"."description") AS "count"
    FROM "action_points_actionpoint"
    LEFT OUTER JOIN "categories_category" ON ("action_points_actionpoint"."category_id" = "categories_category"."id")
    WHERE "action_points_actionpoint"."engagement_id" in (##LIST_OF_ENAGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY "action_points_actionpoint"."engagement_id", "categories_category"."description"
    ORDER BY "action_points_actionpoint"."engagement_id", "categories_category"."description" ASC
    """

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = AuditAudit.objects.select_related(
            "engagement_ptr",
            "engagement_ptr__agreement__auditor_firm__organization",
        )

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                record.id = record.engagement_ptr_id
                record.sub_type = AuditAudit
                record.engagement_ptr._impl = record
                filters = self.config.key(self, record.engagement_ptr)
                values = self.get_values(record.engagement_ptr)
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def get_financial_findings_count(self, record, values, field_name):
        qs = AuditFinancialfinding.objects.filter(audit=record._impl)
        values["financial_findings_amount"] = 0 or qs.aggregate(Sum("amount"))["amount__sum"]
        try:
            perc = 100 * record._impl.financial_findings / record._impl.audited_expenditure
        except (TypeError, DivisionByZero, InvalidOperation):
            perc = 0
        values["percent_of_audited_expenditure"] = perc
        values["pending_unsupported_amount"] = (
            record._impl.financial_findings
            - record.amount_refunded
            - record.additional_supporting_documentation_provided
            - record.justification_provided_and_accepted
            - record.write_off_required
        )

        return qs.count()

    def get_financial_findings_by_category(self, record, values, field_name):
        return []

    def get_key_internal_control_count(self, record, values, field_name):
        return AuditKeyinternalcontrol.objects.filter(audit=record._impl).count()

    def get_key_internal_control_by_category(self, record, values, field_name):
        return []


class Audit(EtoolsDataMartModel):
    created = models.DateField(blank=True, null=True)
    TYPE_AUDIT = "audit"

    TYPES = Choices(
        (TYPE_AUDIT, _("Audit")),
    )

    reference_number = models.CharField(max_length=100, blank=True, null=True)
    engagement_type = models.CharField(max_length=300, blank=True, null=True, choices=TYPES, db_index=True)
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # Engagement Overview Card
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    partner = JSONField(blank=True, null=True, default=dict)
    shared_ip_with = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        verbose_name=_("Shared Audit with"),
    )
    total_value = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)
    date_of_final_report = models.DateField(null=True, blank=True)

    # Audit - Report Section
    audited_expenditure = models.DecimalField(
        verbose_name=_("Audited Expenditure $"), blank=True, null=True, decimal_places=2, max_digits=20
    )
    audited_expenditure_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    financial_findings_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    audit_opinion = models.CharField(max_length=254, blank=True, null=True)
    justification_provided_and_accepted = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    write_off_required = models.DecimalField("Impairment", max_digits=20, decimal_places=2, blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    pending_unsupported_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    percent_of_audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    test_subject_areas_count = models.IntegerField(blank=True, null=True)

    financial_findings = models.DecimalField(
        verbose_name=_("Financial Findings $"), blank=True, null=True, decimal_places=2, max_digits=20
    )
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
        depends = (Partner,)
        mapping = dict(
            auditor="agreement.auditor_firm.organization.name",
            auditor_number="agreement.auditor_firm.organization.vendor_number",
            agreement="agreement.order_number",  # PurchaseOrder
            financial_findings="_impl.financial_findings",
            audit_opinion="_impl.audit_opinion",
            audited_expenditure="_impl.audited_expenditure",
            partner="-",
            financial_findings_count="-",
            key_internal_control_count="-",
            financial_findings_amount="i",
            percent_of_audited_expenditure="i",
            pending_unsupported_amount="i",
            test_subject_areas_count="i",
            action_points="-",
            action_points_data="i",
            key_internal_control_by_category="-",
            financial_findings_by_category="-",
        )
