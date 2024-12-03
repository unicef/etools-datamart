from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, JSONField
from django.utils.translation import gettext as _

from celery.utils.log import get_task_logger
from model_utils import Choices

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import AuditEngagement, AuditFinding, AuditSpotcheck

from .partner import Partner

logger = get_task_logger(__name__)


class SpotCheckLoader(EngagementMixin, EtoolsLoader):
    """
    -- Set country schema
    SET search_path = public, ##COUNTRY##;
    -- Count for paging;
    SELECT COUNT(*) AS "__count" FROM "audit_spotcheck";

    -- Paged retreival of main recordset
    SELECT '##COUNTRY##' AS __schema,
           "audit_spotcheck"."engagement_ptr_id",
           "audit_spotcheck"."total_amount_tested",
           "audit_spotcheck"."total_amount_of_ineligible_expenditure",
           "audit_spotcheck"."internal_controls",

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
           "organizations_organization"."parent_id"
    FROM "audit_spotcheck" INNER JOIN "audit_engagement" ON ("audit_spotcheck"."engagement_ptr_id" = "audit_engagement"."id")
    INNER JOIN "purchase_order_purchaseorder" ON ("audit_engagement"."agreement_id" = "purchase_order_purchaseorder"."id")
    INNER JOIN "purchase_order_auditorfirm" ON ("purchase_order_purchaseorder"."auditor_firm_id" = "purchase_order_auditorfirm"."id")
    INNER JOIN "organizations_organization" ON ("purchase_order_auditorfirm"."organization_id" = "organizations_organization"."id")
    ORDER BY "audit_spotcheck"."engagement_ptr_id" ASC LIMIT ##PAGE_SIZE## OFSET ##PAGE_OFSET##;


    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_offices"."id",
           "audit_engagement_offices"."engagement_id",
           "audit_engagement_offices"."office_id"
    FROM "audit_engagement_offices"
    WHERE "audit_engagement_offices"."engagement_id" IN (##ENGAGEMENT_IDs_IN_THE_PAGE##);

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
    FROM "partners_partnerorganization"
    WHERE "partners_partnerorganization"."id" in (##PARTNER_ORGANIZATION_IDs_IN_THE_PAGE##)

    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_sections"."id",
           "audit_engagement_sections"."engagement_id",
           "audit_engagement_sections"."section_id"
    FROM "audit_engagement_sections"
    WHERE "audit_engagement_sections"."engagement_id" IN (##ENGAGEMENT_IDs_IN_THE_PAGE##);

    SELECT "audit_finding"."spot_check_id".
           "audit_finding"."category_of_observation",
           COUNT("audit_finding"."category_of_observation") AS "count"
    FROM "audit_finding" WHERE ("audit_finding"."priority" = 'high'
          AND "audit_finding"."spot_check_id"  in ( ##SPOTECHECK_IDs_IN_T?HE_PAGE##)  )
    GROUP BY "audit_finding"."spot_check_id", "audit_finding"."category_of_observation"
    ORDER BY "audit_finding"."spot_check_id", "audit_finding"."category_of_observation" ASC


    SELECT "audit_finding"."spot_check_id".
           "audit_finding"."category_of_observation",
           COUNT("audit_finding"."category_of_observation") AS "count"
    FROM "audit_finding" WHERE ("audit_finding"."priority" = 'low'
          AND "audit_finding"."spot_check_id"  in ( ##SPOTECHECK_IDs_IN_THE_PAGE##)  )
    GROUP BY "audit_finding"."spot_check_id", "audit_finding"."category_of_observation"
    ORDER BY "audit_finding"."spot_check_id", "audit_finding"."category_of_observation" ASC


    SELECT "action_points_actionpoint"."engagement_id",
           "action_points_actionpoint"."status",
           COUNT("action_points_actionpoint"."status") AS "count"
    FROM "action_points_actionpoint"
    WHERE "action_points_actionpoint"."engagement_id" IN (##ENGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY "action_points_actionpoint"."engagement_id","action_points_actionpoint"."status"
    ORDER BY "action_points_actionpoint"."engagement_id","action_points_actionpoint"."status" ASC;


    SELECT action_points_actionpoint"."engagement_id"
           "action_points_actionpoint"."high_priority",
           COUNT("action_points_actionpoint"."high_priority") AS "count"
    FROM "action_points_actionpoint"
    WHERE "action_points_actionpoint"."engagement_id" IN (##ENGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY action_points_actionpoint"."engagement_id","action_points_actionpoint"."high_priority"
    ORDER BY action_points_actionpoint"."engagement_id"."action_points_actionpoint"."high_priority" ASC


    SELECT "categories_category"."id",
           "categories_category"."description",
           COUNT("categories_category"."description") AS "count"
    FROM "action_points_actionpoint"
    LEFT OUTER JOIN "categories_category" ON ("action_points_actionpoint"."category_id" = "categories_category"."id")
    WHERE "action_points_actionpoint"."engagement_id" IN (##ENGAGEMENT_IDs_IN_THE_PAGE##)
    GROUP BY "categories_category"."id", "categories_category"."description"
    ORDER BY "categories_category"."id", "categories_category"."description" ASC
    """

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = AuditSpotcheck.objects.select_related(
            "engagement_ptr",
            "engagement_ptr__agreement__auditor_firm__organization",
        ).prefetch_related(
            "engagement_ptr__AuditEngagementOffices_engagement",
        )

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                record.id = record.engagement_ptr_id
                record.sub_type = AuditSpotcheck
                record.engagement_ptr._impl = record
                filters = self.config.key(self, record.engagement_ptr)
                values = self.get_values(record.engagement_ptr)
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def _get_priority_findings(self, record: AuditEngagement, priority: str):
        # TODO: Prefetch  related AuditFinding
        return list(
            AuditFinding.objects.filter(
                spot_check=record._impl,
                priority=priority,
            )
            .order_by("category_of_observation")
            .values("category_of_observation")
            .annotate(
                count=Count("category_of_observation"),
            )
        )

    def get_high_priority_findings(self, record: AuditSpotcheck, values: dict, **kwargs):
        return self._get_priority_findings(record, "high")

    def get_low_priority_findings(self, record: AuditSpotcheck, values: dict, **kwargs):
        return self._get_priority_findings(record, "low")

    def get_pending_unsupported_amount(self, record, values, field_name):
        return (
            record._impl.total_amount_of_ineligible_expenditure
            - record.additional_supporting_documentation_provided
            - record.justification_provided_and_accepted
            - record.write_off_required
            - record.amount_refunded
        )


class SpotCheckFindings(EtoolsDataMartModel):
    TYPE_SPOT_CHECK = "sc"

    TYPES = Choices(
        (TYPE_SPOT_CHECK, _("Spot Check")),
    )
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    created = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )

    # Overview Section
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    partner = JSONField(blank=True, null=True, default=dict)

    total_value = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    amount_refunded = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    write_off_required = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    pending_unsupported_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    # Overview Card
    spotcheck_total_amount_tested = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    spotcheck_total_amount_of_ineligible_expenditure = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=20
    )
    additional_supporting_documentation_provided = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=20
    )
    justification_provided_and_accepted = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)

    # Report Section
    high_priority_findings = JSONField(blank=True, null=True, default=dict)
    low_priority_findings = JSONField(blank=True, null=True, default=dict)

    date_of_field_visit = models.DateField(blank=True, null=True)
    partner_contacted_at = models.DateField(blank=True, null=True)
    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    date_of_comments_by_ip = models.DateField(blank=True, null=True)
    date_of_draft_report_to_unicef = models.DateField(blank=True, null=True)
    date_of_comments_by_unicef = models.DateField(blank=True, null=True)
    date_of_report_submit = models.DateField(blank=True, null=True)
    date_of_final_report = models.DateField(null=True, blank=True)
    date_of_cancel = models.DateField(blank=True, null=True)

    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)

    # Action Points
    action_points = JSONField(blank=True, null=True, default=dict)
    action_points_data = JSONField(blank=True, null=True, default=dict)

    loader = SpotCheckLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditSpotcheck
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            auditor="agreement.auditor_firm.organization.name",
            auditor_number="agreement.auditor_firm.organization.vendor_number",
            spotcheck_total_amount_tested="_impl.total_amount_tested",
            spotcheck_total_amount_of_ineligible_expenditure="_impl.total_amount_of_ineligible_expenditure",
            partner="-",
            sections="-",
            pending_unsupported_amount="-",
            high_priority_findings="-",
            low_priority_findings="-",
            action_points="-",
            action_points_data="i",
        )
