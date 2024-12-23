# PartnersInterventionreview
# PartnersPrcofficerinterventionreview
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import PartnersInterventionreview


class InterventionReviewLoader(EtoolsLoader):
    """
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "partners_interventionreview";

    -- TODO: Pick only the required fields
    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_interventionreview"."id",                  -- to source_id
           "partners_interventionreview"."created",             -- to review_created
           "partners_interventionreview"."modified",            -- to review_modified
           "partners_interventionreview"."review_type",
           "partners_interventionreview"."overall_approval",
           "partners_interventionreview"."amendment_id",
           "partners_interventionreview"."intervention_id",
           "partners_interventionreview"."actions_list",
           "partners_interventionreview"."budget_is_aligned",
           "partners_interventionreview"."ges_considered",
           "partners_interventionreview"."meeting_date",
           "partners_interventionreview"."overall_approver_id", -- to overall_approver = get approver and set "{0.last_name} {0.first_name} ({0.email})".format(record.overall_approver) to overall_approver
           "partners_interventionreview"."overall_comment",
           "partners_interventionreview"."partner_comparative_advantage", -- to partner_comparative_advantage
           "partners_interventionreview"."pd_is_guided",                  -- to pd_is_guided
           "partners_interventionreview"."pd_is_relevant",                -- to pd_is_relevant
           "partners_interventionreview"."relationship_is_represented",   -- to relationship_is_represented
           "partners_interventionreview"."relationships_are_positive",    -- to relationships_are_positive
           "partners_interventionreview"."supply_issues_considered",
           "partners_interventionreview"."submitted_by_id",     -- to overall_approver = get submitted_by and set "{0.last_name} {0.first_name} ({0.email})".format(record.submitted_by)
           "partners_interventionreview"."review_date",         -- to review_date
           "partners_interventionreview"."sent_back_comment",   -- to sent_back_comment

           'syria' AS __schema, "partners_intervention"."id",
           "partners_intervention"."created",
           "partners_intervention"."modified",
           "partners_intervention"."document_type",
           "partners_intervention"."number",            --   to pd_number
           "partners_intervention"."title",             --   to title
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
           "partners_intervention"."partner_authorized_officer_signatory_id",

           "partners_agreement"."id",
           "partners_agreement"."created",
           "partners_agreement"."modified",
           "partners_agreement"."start",
           "partners_agreement"."end",
           "partners_agreement"."agreement_type",
           "partners_agreement"."agreement_number",
           "partners_agreement"."attached_agreement",
           "partners_agreement"."signed_by_unicef_date",
           "partners_agreement"."signed_by_partner_date",
           "partners_agreement"."partner_id",
           "partners_agreement"."signed_by_id",
           "partners_agreement"."status",
           "partners_agreement"."country_programme_id",
           "partners_agreement"."reference_number_year",
           "partners_agreement"."special_conditions_pca",
           "partners_agreement"."terms_acknowledged_by_id",
           "partners_agreement"."partner_manager_id",

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
           "organizations_organization"."name",                     --  to partner
           "organizations_organization"."vendor_number",            --  to partner_vendor_number
           "organizations_organization"."organization_type",        --  to partner_type
           "organizations_organization"."cso_type",                 --  to partner_cso_type
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id"

    FROM "partners_interventionreview"
    INNER JOIN "partners_intervention" ON ("partners_interventionreview"."intervention_id" = "partners_intervention"."id")
    INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_agreement"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    ORDER BY "partners_interventionreview"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;


    """

    def get_overall_approver(self, record: PartnersInterventionreview, values: dict, **kwargs):
        if record.overall_approver:
            return "{0.last_name} {0.first_name} ({0.email})".format(record.overall_approver)

    def get_submitted_by(self, record: PartnersInterventionreview, values: dict, **kwargs):
        if record.submitted_by:
            return "{0.last_name} {0.first_name} ({0.email})".format(record.submitted_by)


class InterventionReview(InterventionSimpleAbstract, EtoolsDataMartModel):
    review_created = models.DateTimeField()
    review_modified = models.DateTimeField()
    review_type = models.CharField(max_length=50, blank=True, null=True)
    overall_approval = models.BooleanField(blank=True, null=True)
    # amendment = models.ForeignKey(PartnersInterventionamendment, models.DO_NOTHING, related_name='PartnersInterventionreview_amendment', blank=True, null=True)

    actions_list = models.TextField(blank=True, null=True)
    budget_is_aligned = models.CharField(max_length=100, blank=True, null=True)
    ges_considered = models.CharField(max_length=100, blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    overall_approver = models.CharField(max_length=2048, blank=True, null=True)
    overall_comment = models.TextField(blank=True, null=True)
    partner_comparative_advantage = models.CharField(max_length=100, blank=True, null=True)
    pd_is_guided = models.CharField(max_length=100, blank=True, null=True)
    pd_is_relevant = models.CharField(max_length=100, blank=True, null=True)
    relationship_is_represented = models.CharField(max_length=10, blank=True, null=True)
    relationships_are_positive = models.CharField(max_length=100, blank=True, null=True)
    supply_issues_considered = models.CharField(max_length=100, blank=True, null=True)
    submitted_by = models.CharField(max_length=2048, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    sent_back_comment = models.TextField(blank=True, null=True)

    loader = InterventionReviewLoader()

    class Options:
        source = PartnersInterventionreview
        depends = (Intervention,)
        mapping = dict(
            pd_number="intervention.number",
            pd_title="intervention.title",
            partner="intervention.agreement.partner.organization.name",
            partner_cso_type="intervention.agreement.partner.organization.cso_type",
            partner_type="intervention.agreement.partner.organization.organization_type",
            partner_vendor_number="intervention.agreement.partner.organization.vendor_number",
            review_created="created",
            review_modified="modified",
            overall_approver="-",
            submitted_by="-",
        )
        queryset = lambda: PartnersInterventionreview.objects.select_related(
            "intervention",
            "intervention__agreement",
            "intervention__agreement__partner",
            "intervention__agreement__partner__organization",
        )
