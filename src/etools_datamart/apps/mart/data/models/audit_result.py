from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import (
    AuditAudit,
    AuditFinancialfinding,
    AuditKeyinternalcontrol,
    AuditRisk,
)


class AuditResultLoader(EtoolsLoader):
    """
    --
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "audit_microassessment";

    --
    SELECT '##COUNTRY##' AS __schema,
           "audit_audit"."id",
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
           "partners_partnerorganization"."organization_id",

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
    FROM "audit_audit"
         INNER JOIN "audit_engagement" ON ("audit_audit"."engagement_ptr_id" = "audit_engagement"."id")
         INNER JOIN "partners_partnerorganization" ON ("audit_engagement"."partner_id" = "partners_partnerorganization"."id")
         INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    ORDER BY "audit_audit"."engagement_ptr_id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT *
    FROM "audit_risk"
    WHERE ("audit_risk"."engagement_id" IN (##LIST OF "audit_audit"."id" IN THE PAGE##)
    AND "audit_risk"."value" = 4);

    --
    SELECT *
    FROM "audit_financialfinding"
    WHERE "audit_financialfinding"."audit_id" IN (##LIST OF "audit_audit"."id" IN THE PAGE##);

    --
    SELECT *
    FROM "audit_keyinternalcontrol"
    WHERE "audit_keyinternalcontrol"."audit_id" IN (##LIST OF "audit_audit"."id" IN THE PAGE##);
    """

    def get_mart_values(self, record: AuditAudit = None):
        ret = super().get_mart_values(None)
        ret["source_id"] = record.engagement_ptr_id
        return ret

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "engagement_ptr",
                "engagement_ptr__partner",
                "engagement_ptr__partner__organization",
            )
        )

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
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    # AuditAudit.engagement_ptr.partner.partner_type - -
    partner_type = models.CharField(max_length=300, blank=True, null=True)

    # AuditAudit.engagement_ptr.partner.rating
    risk_rating = models.CharField(max_length=50, blank=True, null=True)

    # AuditAudit.audited_expenditure
    audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2)

    # AuditAudit.financial_findings - -
    financial_findings = models.DecimalField(max_digits=20, decimal_places=2)

    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    additional_supporting_documentation_provided = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    justification_provided_and_accepted = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    write_off_required = models.DecimalField("Impairment", max_digits=20, decimal_places=2, blank=True, null=True)
    pending_unsupported_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    # AuditAudit.audit_opinion - -
    audit_opinion = models.CharField(max_length=20)

    #  AuditAudit.engagement_ptr.filter(AuditRisk_engagement=4)
    count_high_risk_findings = models.IntegerField(blank=True, null=True)

    #  model count(Audit.FinancialFinding) per engagement.
    count_financial_findings = models.IntegerField(blank=True, null=True)

    # model count(Audit.KeyInternalControl) per engagement
    count_key_control_weaknesses = models.IntegerField(blank=True, null=True)

    status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )

    loader = AuditResultLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditAudit
        sync_deleted_records = lambda loader: False
        mapping = {
            "source_id": "engagement_ptr.id",
            "vendor": "engagement_ptr.partner.organization.name",
            "status": "engagement_ptr.status",
            "vendor_number": "engagement_ptr.partner.organization.vendor_number",
            "partner_type": "engagement_ptr.partner.organization.organization_type",
            "risk_rating": "engagement_ptr.partner.rating",
            "date_of_draft_report_to_ip": "engagement_ptr.date_of_draft_report_to_ip",
            "amount_refunded": "engagement_ptr.amount_refunded",
            "additional_supporting_documentation_provided": "engagement_ptr.additional_supporting_documentation_provided",
            "justification_provided_and_accepted": "engagement_ptr.justification_provided_and_accepted",
            "write_off_required": "engagement_ptr.write_off_required",
            "pending_unsupported_amount": "engagement_ptr.pending_unsupported_amount",
            "audited_expenditure": "=",
            "financial_findings": "=",
            "audit_opinion": "=",
            "count_high_risk_findings": "-",
            "count_financial_findings": "-",
            "count_key_control_weaknesses": "-",
        }
