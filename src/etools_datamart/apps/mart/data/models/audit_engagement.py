from django.contrib.postgres.fields import ArrayField
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, JSONField, Prefetch
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts, RiskConst
from etools_datamart.apps.sources.etools.models import (
    ActionPointsActionpoint,
    AuditAudit,
    AuditEngagement,
    AuditEngagementActivePd,
    AuditEngagementSections,
    AuditMicroassessment,
    AuditRisk,
    AuditSpecialaudit,
    AuditSpotcheck,
    DjangoContentType,
    UnicefAttachmentsAttachment,
)

from .partner import Partner

attachment_codes = {
    AuditAudit: "audit_final_report",
    AuditMicroassessment: "micro_assessment_final_report",
    AuditSpecialaudit: "special_audit_final_report",
    AuditSpotcheck: "spotcheck_final_report",
}

URLMAP = {
    "AuditSpotcheck": "%s/ap/spot-checks/%s/overview/?schema=%s",
    "AuditMicroassessment": "%s/ap/micro-assessments/%s/overview/?schema=%s",
    "AuditSpecialaudit": "%s/ap/special-audits/%s/overview/?schema=%s",
    "AuditAudit": "%s/ap/audits/%s/overview/?schema=%s",
    "TpmTpmactivity": "%s/t2f/edit-travel/%s/?schema=%s",
    "T2FTravelactivity": "%s/t2f/edit-travel/%s/?schema=%s",
}

MODULEMAP = {
    "AuditSpotcheck": "fam",
    "AuditMicroassessment": "fam",
    "AuditSpecialaudit": "fam",
    "AuditAudit": "fam",
    "TpmTpmactivity": "tpm",
    "T2FTravelactivity": "trips",
}


class EngagementMixin:
    OVERALL_RISK_MAP = {}

    def get_partner(self, record: AuditEngagement, values: dict, **kwargs):
        try:
            p = Partner.objects.get(schema_name=self.context["country"].schema_name, source_id=record.partner.pk)
            return {
                "name": p.name,
                "vendor_number": p.vendor_number,
                "id": p.pk,
                "source_id": p.source_id,
                "type": p.partner_type,
                "cso_type": p.cso_type,
                "reported_cy": str(p.reported_cy),
                "total_ct_cy": str(p.total_ct_cy),
            }
        except Partner.DoesNotExist:
            return {
                key: "N/A"
                for key in [
                    "name",
                    "vendor_number",
                    "id",
                    "source_id",
                    "type",
                    "cso_type",
                    "reported_cy",
                    "total_ct_cy",
                ]
            }

    def _get_risk(self, record: AuditEngagement, **kwargs):
        try:
            risk = AuditRisk.objects.get(engagement=record, **kwargs)
            extra = risk.extra
            value = risk.value
            text = RiskConst.VALUES[value]
        except AuditRisk.DoesNotExist:
            extra, value, text = "", "", ""
        return value, extra, text

    def _get_risks(self, record: AuditEngagement, **kwargs):
        try:
            risks = AuditRisk.objects.filter(engagement=record, **kwargs)
            value = ", ".join([risk.blueprint.header for risk in risks])
            count = risks.count()
        except AuditRisk.DoesNotExist:
            value, count = "", -1
        return value, count

    def get_rating(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {"blueprint__category__code": "ma_global_assessment"}
        value, extra, text = self._get_risk(record, **filters)
        values["rating_extra"] = extra
        return text

    def get_sections(self, record: AuditEngagement, values: dict, **kwargs):
        data = []
        for rec in record.AuditEngagementSections_engagement.all():
            data.append(
                dict(
                    source_id=rec.section.pk,
                    name=rec.section.name,
                    description=rec.section.description,
                ),
            )
        values["sections_data"] = data
        return ", ".join([loc["name"] for loc in data])

    def get_offices(self, record: AuditEngagement, values: dict, **kwargs):
        data = []
        for rec in record.AuditEngagementOffices_engagement.all():
            data.append(
                dict(
                    source_id=rec.office.id,
                    name=rec.office.name,
                )
            )
        values["offices_data"] = data
        return ", ".join([office["name"] for office in data])

    def get_action_points(self, record, values, **kwargs):
        aggr = "category__description"
        st, pr = "status", "high_priority"
        qs = ActionPointsActionpoint.objects.filter(engagement=record)
        by_status = list(qs.order_by(st).values(st).annotate(count=Count(st)))
        by_priority = list(qs.order_by(pr).values(pr).annotate(count=Count(pr)))
        values["action_points_data"] = by_status + by_priority
        return list(qs.order_by(aggr).values(aggr).annotate(count=Count(aggr)))

    def get_status(self, record, values, **kwargs):
        if record.status != AuditEngagementConsts.STATUSES.partner_contacted:
            return record.status
        if record.date_of_comments_by_unicef:
            return record.DISPLAY_STATUSES.comments_received_by_unicef
        elif record.date_of_draft_report_to_unicef:
            return record.DISPLAY_STATUSES.draft_issued_to_unicef
        elif record.date_of_comments_by_ip:
            return record.DISPLAY_STATUSES.comments_received_by_partner
        elif record.date_of_draft_report_to_ip:
            return record.DISPLAY_STATUSES.draft_issued_to_partner
        elif record.date_of_field_visit:
            return record.DISPLAY_STATUSES.field_visit

        return record.status


class EngagementlLoader(EngagementMixin, EtoolsLoader):
    """
    -- Set country schema
    SET search_path = public, ##COUNTRY##;

    -- Count for paging;
    SELECT COUNT(*) AS "__count" FROM "audit_engagement";

    -- Audit

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

           "purchase_order_purchaseorderitem"."id",
           "purchase_order_purchaseorderitem"."number",
           "purchase_order_purchaseorderitem"."purchase_order_id"

    FROM "audit_microassessment"
         INNER JOIN "audit_engagement" ON ("audit_microassessment"."engagement_ptr_id" = "audit_engagement"."id")
         INNER JOIN "partners_partnerorganization" ON ("audit_engagement"."partner_id" = "partners_partnerorganization"."id")
         INNER JOIN "purchase_order_purchaseorder" ON ("audit_engagement"."agreement_id" = "purchase_order_purchaseorder"."id")
         INNER JOIN "purchase_order_auditorfirm" ON ("purchase_order_purchaseorder"."auditor_firm_id" = "purchase_order_auditorfirm"."id")
         INNER JOIN "organizations_organization" ON ("purchase_order_auditorfirm"."organization_id" = "organizations_organization"."id")
         LEFT OUTER JOIN "purchase_order_purchaseorderitem" ON ("audit_engagement"."po_item_id" = "purchase_order_purchaseorderitem"."id")
    ORDER BY "audit_engagement"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    -- Authorized officers for the page
    SELECT ("audit_engagement_authorized_officers"."engagement_id") AS "_prefetch_related_val_engagement_id",
           "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined",
           "auth_user"."middle_name",
           "auth_user"."created",
           "auth_user"."modified",
           "auth_user"."preferences"
    FROM "auth_user"
         INNER JOIN "audit_engagement_authorized_officers" ON ("auth_user"."id" = "audit_engagement_authorized_officers"."user_id")
    WHERE "audit_engagement_authorized_officers"."engagement_id" IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE## );

    -- Authorized staff members for the page
    SELECT ("audit_engagement_staff_members"."engagement_id") AS "_prefetch_related_val_engagement_id",
           "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined",
           "auth_user"."middle_name",
           "auth_user"."created",
           "auth_user"."modified",
           "auth_user"."preferences"
    FROM "auth_user"
         INNER JOIN "audit_engagement_staff_members" ON ("auth_user"."id" = "audit_engagement_staff_members"."user_id")
    WHERE "audit_engagement_staff_members"."engagement_id" IN IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE## );


    -- Audit Engagement Sections for the page
    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_sections"."id",
           "audit_engagement_sections"."engagement_id",
           "audit_engagement_sections"."section_id"
    FROM "audit_engagement_sections"
    WHERE "audit_engagement_sections"."engagement_id" IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE## );


    -- action_points_actionpoint for the page
    SELECT '##COUNTRY##' AS __schema, "action_points_actionpoint"."id",
           "action_points_actionpoint"."created",
           "action_points_actionpoint"."modified",
           "action_points_actionpoint"."status",
           "action_points_actionpoint"."description",
           "action_points_actionpoint"."due_date",
           "action_points_actionpoint"."date_of_completion",
           "action_points_actionpoint"."assigned_by_id",
           "action_points_actionpoint"."assigned_to_id",
           "action_points_actionpoint"."author_id",
           "action_points_actionpoint"."cp_output_id",
           "action_points_actionpoint"."engagement_id",
           "action_points_actionpoint"."intervention_id",
           "action_points_actionpoint"."location_id",
           "action_points_actionpoint"."office_id",
           "action_points_actionpoint"."partner_id",
           "action_points_actionpoint"."section_id",
           "action_points_actionpoint"."tpm_activity_id",
           "action_points_actionpoint"."high_priority",
           "action_points_actionpoint"."travel_activity_id",
           "action_points_actionpoint"."category_id",
           "action_points_actionpoint"."psea_assessment_id",
           "action_points_actionpoint"."reference_number",
           "action_points_actionpoint"."monitoring_activity_id"
    FROM "action_points_actionpoint"
    WHERE "action_points_actionpoint"."engagement_id" IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE## );


    -- audit_engagement_active_pd for the page
    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_active_pd"."id",
           "audit_engagement_active_pd"."engagement_id",
           "audit_engagement_active_pd"."intervention_id"
    FROM "audit_engagement_active_pd"
    WHERE "audit_engagement_active_pd"."engagement_id" IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE## );


    --
    SELECT '##COUNTRY##' AS __schema, "audit_risk"."id",
           "audit_risk"."value",
           "audit_risk"."extra",
           "audit_risk"."blueprint_id",
           "audit_risk"."engagement_id"
    FROM "audit_risk"
         INNER JOIN "audit_riskblueprint" ON ("audit_risk"."blueprint_id" = "audit_riskblueprint"."id")
         INNER JOIN "audit_riskcategory" ON ("audit_riskblueprint"."category_id" = "audit_riskcategory"."id")
    WHERE ("audit_riskcategory"."header" = 'Key Internal Controls Weaknesses' AND "audit_risk"."engagement_id"
            IN (##LIST OF ENGAGEMENT_IDs IN THE PAGE##))


    --
    SELECT "organizations_organization"."id",
           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id"
    FROM "organizations_organization" WHERE "organizations_organization"."id"
         IN (##LIST OF "organizations_organization"."id" in tje main recordset IN THE PAGE ## );


    --
    SELECT '##COUNTRY##' AS __schema,
           "audit_engagement_sections"."id",
           "audit_engagement_sections"."engagement_id",
           "audit_engagement_sections"."section_id"
    FROM "audit_engagement_sections"
    WHERE "audit_engagement_sections"."engagement_id" IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE## );


    --
    SELECT "django_content_type"."id",
           "django_content_type"."app_label",
           "django_content_type"."model"
    FROM "django_content_type"
    WHERE ("django_content_type"."app_label" = 'audit' AND "django_content_type"."model" = 'engagement');


    --
    SELECT "unicef_attachments_attachment"."file"
    FROM "unicef_attachments_attachment"
    WHERE ("unicef_attachments_attachment"."code" = 'audit_engagement'
           AND "unicef_attachments_attachment"."content_type_id" = 216
           AND "unicef_attachments_attachment"."object_id" IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE##  )

    --
    SELECT "unicef_attachments_attachment"."file"
    FROM "unicef_attachments_attachment"
    WHERE ("unicef_attachments_attachment"."code" = 'audit_report'
           AND "unicef_attachments_attachment"."content_type_id" = 216
           AND "unicef_attachments_attachment"."object_id"  IN ( ##LIST OF ENGAGEMENT_IDs IN THE PAGE##  )


    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_intervention"."id",
           "partners_intervention"."created",
           "partners_intervention"."modified",
           "partners_intervention"."document_type",
           "partners_intervention"."number",
           "partners_intervention"."title",
           "partners_intervention"."status",
           "partners_intervention"."start",
           "partners_intervention"."end",
           "partners_intervention"."submission_date",
           "partners_intervention"."submission_date_prc",
           "partners_intervention"."review_date_prc",
           "partners_intervention"."prc_review_document",
           "partners_intervention"."signed_by_unicef_date",
           "partners_intervention"."signed_by_partner_date",
           "partners_intervention"."population_focus",
           "partners_intervention"."agreement_id",
           "partners_intervention"."unicef_signatory_id",
           "partners_intervention"."signed_pd_document",
           "partners_intervention"."country_programme_id",
           "partners_intervention"."contingency_pd",
           "partners_intervention"."metadata",
           "partners_intervention"."in_amendment",
           "partners_intervention"."reference_number_year",
           "partners_intervention"."activation_letter",
           "partners_intervention"."termination_doc",
           "partners_intervention"."cfei_number",
           "partners_intervention"."budget_owner_id",
           "partners_intervention"."context",
           "partners_intervention"."date_sent_to_partner",
           "partners_intervention"."equity_narrative",
           "partners_intervention"."equity_rating",
           "partners_intervention"."gender_narrative",
           "partners_intervention"."gender_rating",
           "partners_intervention"."hq_support_cost",
           "partners_intervention"."implementation_strategy",
           "partners_intervention"."ip_program_contribution",
           "partners_intervention"."partner_accepted",
           "partners_intervention"."sustainability_narrative",
           "partners_intervention"."sustainability_rating",
           "partners_intervention"."unicef_accepted",
           "partners_intervention"."unicef_court",
           "partners_intervention"."unicef_review_type",
           "partners_intervention"."humanitarian_flag",
           "partners_intervention"."capacity_development",
           "partners_intervention"."other_info",
           "partners_intervention"."other_partners_involved",
           "partners_intervention"."technical_guidance",
           "partners_intervention"."cash_transfer_modalities",
           "partners_intervention"."cancel_justification",
           "partners_intervention"."date_partnership_review_performed",
           "partners_intervention"."accepted_on_behalf_of_partner",
           "partners_intervention"."activation_protocol",
           "partners_intervention"."confidential",
           "partners_intervention"."has_activities_involving_children",
           "partners_intervention"."has_data_processing_agreement",
           "partners_intervention"."has_special_conditions_for_construction",
           "partners_intervention"."final_review_approved",
           "partners_intervention"."other_details",
           "partners_intervention"."partner_authorized_officer_signatory_id"
    FROM "partners_intervention"
    WHERE   ( "partners_intervention"."id" IN ( ##LIST OF "action_points_actionpoint"."intervention_id" in action_points_actionpoint for the page ## )
              OR  partners_intervention"."id" IN  ( ##LIST OF  "audit_engagement_active_pd"."intervention_id" in audit_engagement_active_pd for the page ## )
            );

    """

    def get_content_type(self, sub_type):
        mapping = {
            AuditAudit: "audit",
            AuditEngagement: "engagement",
            AuditMicroassessment: "microassessment",
            AuditSpecialaudit: "specialaudit",
            AuditSpotcheck: "spotcheck",
        }
        return DjangoContentType.objects.get(app_label="audit", model=mapping[sub_type])

    def get_engagement_attachments(self, record: AuditEngagement, values: dict, **kwargs):
        # audit_engagement
        ret = UnicefAttachmentsAttachment.objects.filter(
            object_id=record.id, code="audit_engagement", content_type=self.get_content_type(AuditEngagement)
        ).values_list("file", flat=True)

        return ", ".join(ret)

    def get_report_attachments(self, record: AuditEngagement, values: dict, **kwargs):
        # audit_report
        ret = UnicefAttachmentsAttachment.objects.filter(
            object_id=record.id, code="audit_report", content_type=self.get_content_type(AuditEngagement)
        ).values_list("file", flat=True)

        return ", ".join(ret)

    def get_final_report(self, record: AuditEngagement, values: dict, **kwargs):
        if getattr(record._impl, "final_report", None):
            return UnicefAttachmentsAttachment.objects.get(
                object_id=record.id,
                code=attachment_codes[record.sub_type],
                content_type=self.get_content_type(record.sub_type),
            ).file

    def get_values(self, record: AuditEngagement):
        values = {}
        self.mapping.update(**values)
        return super().get_values(record)

    def get_authorized_officers(self, record: AuditEngagement, values: dict, **kwargs):
        ret = []
        for o in record.authorized_officers.all():
            ret.append(
                {
                    "last_name": o.last_name,
                    "first_name": o.first_name,
                    "partner": record.partner.organization.name,
                    "email": o.email,
                }
            )
        values["authorized_officers_data"] = ret
        return ", ".join([o["email"] for o in ret])

    def get_active_pd(self, record: AuditEngagement, values: dict, **kwargs):
        ret = []
        for o in record.prefetched_AuditEngagementActivePds:
            ret.append(
                {
                    "title": o.intervention.title,
                    "number": o.intervention.number,
                    "status": o.intervention.status,
                    "document_type": o.intervention.document_type,
                }
            )

        values["active_pd_data"] = ret
        return ", ".join([o["number"] for o in ret])

    def get_partner_id(self, record: AuditEngagement, values: dict, **kwargs):
        try:
            return Partner.objects.get(schema_name=self.context["country"].schema_name, source_id=record.partner.id).pk
        except Partner.DoesNotExist:
            return None

    def get_staff_members(self, record: AuditEngagement, values: dict, **kwargs):
        ret = []
        for o in record.staff_members.all():
            ret.append(
                {
                    "last_name": o.last_name,
                    "first_name": o.first_name,
                    "email": o.email,
                }
            )
        values["staff_members_data"] = ret
        return ", ".join([o["email"] for o in ret])

    # def get_active_pd(self, original: AuditEngagement, values: dict):
    #     return None

    def get_action_points(self, record: AuditEngagement, values: dict, **kwargs):
        from etools_datamart.api.endpoints.datamart.actionpoint import ActionPointSimpleSerializer

        ret = []
        for r in record.prefetched_ActionPoints:
            ret.append(ActionPointSimpleSerializer(r).data)
        return ret

    def get_key_internal_control_weaknesses(self, record: AuditEngagement, values: dict, **kwargs):
        risks = []

        for risk in record.prefetched_AuditRisks:
            risks.append(risk.blueprint.header)

        return risks

    def process_country(self):
        # TODO: Analyze more before batch processing
        for m in [AuditMicroassessment, AuditSpecialaudit, AuditSpotcheck, AuditAudit]:
            for record in m.objects.select_related(
                "engagement_ptr",
                "engagement_ptr__partner",
                "engagement_ptr__agreement",
                "engagement_ptr__agreement__auditor_firm",
                "engagement_ptr__agreement__auditor_firm__organization",
                "engagement_ptr__po_item",
            ).prefetch_related(
                "engagement_ptr__authorized_officers",
                "engagement_ptr__staff_members",
                Prefetch(
                    "engagement_ptr__AuditEngagementSections_engagement",
                    AuditEngagementSections.objects.all(),
                    to_attr="prefetched_AuditEngagementSections",
                ),
                Prefetch(
                    "engagement_ptr__ActionPointsActionpoint_engagement",
                    ActionPointsActionpoint.objects.all(),
                    to_attr="prefetched_ActionPoints",
                ),
                Prefetch(
                    "engagement_ptr__AuditEngagementActivePd_engagement",
                    AuditEngagementActivePd.objects.all(),
                    to_attr="prefetched_AuditEngagementActivePds",
                ),
                Prefetch(
                    "engagement_ptr__AuditRisk_engagement",
                    AuditRisk.objects.filter(blueprint__category__header="Key Internal Controls Weaknesses"),
                    to_attr="prefetched_AuditRisks",
                ),
            ):
                record.id = record.engagement_ptr_id
                record.sub_type = m
                record.engagement_ptr._impl = record
                filters = self.config.key(self, record.engagement_ptr)
                values = self.get_values(record.engagement_ptr)
                op = self.process_record(filters, values)
                self.increment_counter(op)


class Engagement(EtoolsDataMartModel):
    TYPE_AUDIT = "audit"
    TYPE_MICRO_ASSESSMENT = "ma"
    TYPE_SPOT_CHECK = "sc"
    TYPE_SPECIAL_AUDIT = "sa"

    TYPES = Choices(
        (TYPE_AUDIT, _("Audit")),
        (TYPE_MICRO_ASSESSMENT, _("Micro Assessment")),
        (TYPE_SPOT_CHECK, _("Spot Check")),
        (TYPE_SPECIAL_AUDIT, _("Special Audit")),
    )

    # DISPLAY_STATUSES = Choices(
    #     ('partner_contacted', _('IP Contacted')),
    #     ('field_visit', _('Field Visit')),
    #     ('draft_issued_to_partner', _('Draft Report Issued to IP')),
    #     ('comments_received_by_partner', _('Comments Received from IP')),
    #     ('draft_issued_to_unicef', _('Draft Report Issued to UNICEF')),
    #     ('comments_received_by_unicef', _('Comments Received from UNICEF')),
    #     ('report_submitted', _('Report Submitted')),
    #     ('final', _('Final Report')),
    #     ('cancelled', _('Cancelled')),
    # )
    # DISPLAY_STATUSES_DATES = {
    #     DISPLAY_STATUSES.partner_contacted: 'partner_contacted_at',
    #     DISPLAY_STATUSES.field_visit: 'date_of_field_visit',
    #     DISPLAY_STATUSES.draft_issued_to_partner: 'date_of_draft_report_to_ip',
    #     DISPLAY_STATUSES.comments_received_by_partner: 'date_of_comments_by_ip',
    #     DISPLAY_STATUSES.draft_issued_to_unicef: 'date_of_draft_report_to_unicef',
    #     DISPLAY_STATUSES.comments_received_by_unicef: 'date_of_comments_by_unicef',
    #     DISPLAY_STATUSES.report_submitted: 'date_of_report_submit',
    #     DISPLAY_STATUSES.final: 'date_of_final_report',
    #     DISPLAY_STATUSES.cancelled: 'date_of_cancel'
    # }

    # Base fields
    active_pd = models.TextField(blank=True, null=True)
    active_pd_data = JSONField(blank=True, null=True)
    additional_supporting_documentation_provided = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=20
    )
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    amount_refunded = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    authorized_officers = models.TextField(blank=True, null=True)
    authorized_officers_data = JSONField(blank=True, null=True)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    cancel_comment = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    date_of_cancel = models.DateField(null=True, blank=True)
    date_of_comments_by_ip = models.DateField(blank=True, null=True)
    date_of_comments_by_unicef = models.DateField(blank=True, null=True)
    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    date_of_draft_report_to_unicef = models.DateField(blank=True, null=True)
    date_of_field_visit = models.DateField(blank=True, null=True)
    date_of_final_report = models.DateField(null=True, blank=True)
    date_of_report_submit = models.DateField(null=True, blank=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)
    engagement_attachments = models.TextField(blank=True, null=True)
    engagement_type = models.CharField(max_length=300, blank=True, null=True, choices=TYPES, db_index=True)
    exchange_rate = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    explanation_for_additional_information = models.TextField(blank=True, null=True)
    joint_audit = models.BooleanField(default=False, blank=True, null=True)
    justification_provided_and_accepted = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    modified = models.DateField(blank=True, null=True)
    partner_contacted_at = models.DateField(blank=True, null=True, db_index=True)
    partner = JSONField(blank=True, null=True, default=dict)
    po_item = models.IntegerField(blank=True, null=True)
    report_attachments = models.TextField(blank=True, null=True)
    staff_members = models.TextField(blank=True, null=True)
    staff_members_data = JSONField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )
    total_value = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    write_off_required = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)

    reference_number = models.CharField(max_length=300, blank=True, null=True)

    # final_report is shared across all Engagement types
    final_report = models.CharField(max_length=300, blank=True, null=True)

    shared_ip_with = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        verbose_name=_("Shared Audit with"),
    )

    # SpotCheck
    spotcheck_total_amount_tested = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    spotcheck_total_amount_of_ineligible_expenditure = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=20
    )
    spotcheck_internal_controls = models.TextField(null=True, blank=True)
    spotcheck_final_report = models.CharField(max_length=300, blank=True, null=True)
    # MicroAssessment
    # final_report = CodedGenericRelation(Attachment, code='micro_assessment_final_report')
    # Audit
    rating = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=RiskConst.VALUES,
    )
    rating_extra = JSONField(blank=True, null=True)

    AUDIT_OPTION_UNQUALIFIED = "unqualified"
    AUDIT_OPTION_QUALIFIED = "qualified"
    AUDIT_OPTION_DENIAL = "disclaimer_opinion"
    AUDIT_OPTION_ADVERSE = "adverse_opinion"

    AUDIT_OPTIONS = Choices(
        (AUDIT_OPTION_UNQUALIFIED, _("Unqualified")),
        (AUDIT_OPTION_QUALIFIED, _("Qualified")),
        (AUDIT_OPTION_DENIAL, _("Disclaimer opinion")),
        (AUDIT_OPTION_ADVERSE, _("Adverse opinion")),
    )

    audited_expenditure = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    financial_findings = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    audit_opinion = models.CharField(max_length=20, choices=AUDIT_OPTIONS, blank=True, null=True, db_index=True)
    # final_report = CodedGenericRelation(Attachment, code='audit_final_report')

    # SpecialAudit
    # final_report = CodedGenericRelation(Attachment, code='special_audit_final_report')

    # ActionPoints
    action_points = JSONField(blank=True, null=True)
    key_internal_control_weaknesses = JSONField(blank=True, null=True)
    year_of_audit = models.SmallIntegerField(blank=True, null=True)

    # datamart
    loader = EngagementlLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditEngagement
        sync_deleted_records = lambda a: False  # noqa
        depends = (Partner,)
        mapping = dict(
            active_pd="-",
            active_pd_data="i",
            agreement="agreement.order_number",  # PurchaseOrder
            auditor="agreement.auditor_firm.organization.name",
            auditor_number="agreement.auditor_firm.organization.vendor_number",
            authorized_officers="-",
            engagement_attachments="-",
            report_attachments="-",
            staff_members="-",
            partner="-",
            po_item="po_item.number",  # PurchaseOrderItem
            final_report="-",
            spotcheck_total_amount_tested="_impl.total_amount_tested",
            spotcheck_total_amount_of_ineligible_expenditure="_impl.total_amount_of_ineligible_expenditure",
            spotcheck_final_report="_impl.final_report",
            spotcheck_internal_controls="_impl.internal_controls",
            audited_expenditure="_impl.audited_expenditure",
            financial_findings="_impl.financial_findings",
            audit_opinion="_impl.audit_opinion",
            action_points="-",
            rating="-",
            rating_extra="i",
            key_internal_control_weaknesses="-",
        )
