from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention import Intervention
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst
from etools_datamart.apps.sources.etools.models import models, PartnersInterventionplannedvisits


class InterventionPlannedVisits(EtoolsDataMartModel):
    """
    --
    SET search_path = public,##COUNTRY##
    --
    SELECT COUNT(*) AS "__count"
    FROM "partners_interventionplannedvisits";

    -- TODO: Pick only the required fields
    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_interventionplannedvisits"."id",
           "partners_interventionplannedvisits"."year",             -- directly mapped to programmatic_year
           "partners_interventionplannedvisits"."programmatic_q4",  -- directly mapped to programmatic_q4
           "partners_interventionplannedvisits"."intervention_id",
           "partners_interventionplannedvisits"."created",
           "partners_interventionplannedvisits"."modified",
           "partners_interventionplannedvisits"."programmatic_q1",  -- directly mapped to programmatic_q1
           "partners_interventionplannedvisits"."programmatic_q2",  -- directly mapped to programmatic_q2
           "partners_interventionplannedvisits"."programmatic_q3",  -- directly mapped to programmatic_q3

           '##COUNTRY##' AS __schema,
           "partners_intervention"."id",
           "partners_intervention"."created",
           "partners_intervention"."modified",
           "partners_intervention"."document_type",
           "partners_intervention"."number",
           "partners_intervention"."title",
           "partners_intervention"."status",                    -- directly mapped to pd_status
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
           "organizations_organization"."name",                  -- directly mapped to partner_name
           "organizations_organization"."vendor_number",         -- directly mapped to partner_vendor_number
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id"
    FROM "partners_interventionplannedvisits"
    INNER JOIN "partners_intervention" ON ("partners_interventionplannedvisits"."intervention_id" = "partners_intervention"."id")
    INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_agreement"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    ORDER BY "partners_interventionplannedvisits"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;
    """

    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    partner_vendor_number = models.CharField(max_length=100, blank=True, null=True)
    partner_name = models.CharField(max_length=200, null=True)
    pd_status = models.CharField(max_length=32, null=True, db_index=True, choices=PartnersInterventionConst.STATUSES)
    pd_reference_number = models.CharField(max_length=100, null=True)

    year = models.IntegerField()
    programmatic_q1 = models.IntegerField(default=0)
    programmatic_q2 = models.IntegerField(default=0)
    programmatic_q3 = models.IntegerField(default=0)
    programmatic_q4 = models.IntegerField(default=0)

    loader = EtoolsLoader()

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Intervention Planned Visits"

    class Options:
        source = PartnersInterventionplannedvisits
        depends = (Intervention,)
        queryset = lambda: PartnersInterventionplannedvisits.objects.select_related(
            "intervention",
            "intervention__agreement",
            "intervention__agreement__partner",
            "intervention__agreement__partner__organization",
        )
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, source_id=record.pk)
        mapping = dict(
            partner_vendor_number="intervention.agreement.partner.organization.vendor_number",
            partner_name="intervention.agreement.partner.organization.name",
            pd_status="intervention.status",
            pd_reference_number="intervention.reference_number",
            year="=",
            programmatic_q1="=",
            programmatic_q2="=",
            programmatic_q3="=",
            programmatic_q4="=",
        )
