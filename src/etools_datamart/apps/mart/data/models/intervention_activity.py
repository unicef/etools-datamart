from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import ReportsInterventionactivityitem


class InterventionActivityLoader(EtoolsLoader):
    pass

    """
    --
    SET search_path = public, ##COUNTRY##;
    
    --
    SELECT COUNT(*) AS "__count" 
    FROM "reports_interventionactivityitem";

    --  
    -- Note: Only very few of number of fields of ORM generated query result set is used. 
    --       Most of the fields can be dropped.   
    SELECT '##COUNTRY##' AS __schema,
            "reports_interventionactivityitem"."id",
            "reports_interventionactivityitem"."created",
            "reports_interventionactivityitem"."modified",
            "reports_interventionactivityitem"."name",        
            "reports_interventionactivityitem"."unicef_cash",
            "reports_interventionactivityitem"."cso_cash",
            "reports_interventionactivityitem"."activity_id",
            "reports_interventionactivityitem"."no_units",
            "reports_interventionactivityitem"."unit",
            "reports_interventionactivityitem"."unit_price",
            "reports_interventionactivityitem"."code",
            
            "reports_interventionactivity"."id",
            "reports_interventionactivity"."created",
            "reports_interventionactivity"."modified",
            "reports_interventionactivity"."name",              -- directly mapped to <target>.activity
            "reports_interventionactivity"."context_details",   -- directly mapped to <target>.activity_details
            "reports_interventionactivity"."unicef_cash",       -- directly mapped to <target>.activity_unicef_cash   
            "reports_interventionactivity"."cso_cash",          -- directly mapped to <target>.activity_cso_cash
            "reports_interventionactivity"."result_id",
            "reports_interventionactivity"."code",              -- directly mapped to <target>.activity_code
            "reports_interventionactivity"."is_active",
            
            "reports_lowerresult"."id",
            "reports_lowerresult"."name",                       -- directly mapped to <target>.ll_name
            "reports_lowerresult"."code",                       -- directly mapped to <target>.ll_code   
            "reports_lowerresult"."result_link_id",
            "reports_lowerresult"."created",
            "reports_lowerresult"."modified",
            "reports_lowerresult"."is_active",
            
            "partners_interventionresultlink"."id",
            "partners_interventionresultlink"."cp_output_id",
            "partners_interventionresultlink"."intervention_id",
            "partners_interventionresultlink"."created",
            "partners_interventionresultlink"."modified", 
            "partners_interventionresultlink"."code",
            
            "partners_intervention"."id",
            "partners_intervention"."created",
            "partners_intervention"."modified",
            "partners_intervention"."document_type",
            "partners_intervention"."number",       -- directly mapped to <target>.pd_number
            "partners_intervention"."title",        -- directly mapped to <target>.pd_title
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
            "organizations_organization"."name",              -- directly mapped to <target>.partner
            "organizations_organization"."vendor_number",     -- directly mapped to <target>.partner_vendor_number  
            "organizations_organization"."organization_type", -- directly mapped to <target>.partner_type 
            "organizations_organization"."cso_type",          -- directly mapped to <target>.partner_cso_type     
            "organizations_organization"."short_name",
            "organizations_organization"."other",
            "organizations_organization"."parent_id" 
    FROM "reports_interventionactivityitem" 
    INNER JOIN "reports_interventionactivity" ON ("reports_interventionactivityitem"."activity_id" = "reports_interventionactivity"."id") 
    INNER JOIN "reports_lowerresult" ON ("reports_interventionactivity"."result_id" = "reports_lowerresult"."id") 
    INNER JOIN "partners_interventionresultlink" ON ("reports_lowerresult"."result_link_id" = "partners_interventionresultlink"."id") 
    INNER JOIN "partners_intervention" ON ("partners_interventionresultlink"."intervention_id" = "partners_intervention"."id") INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_agreement"."id") INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id") INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id") 
    ORDER BY "reports_interventionactivityitem"."id" ASC 
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;
    """


class InterventionActivity(InterventionSimpleAbstract, EtoolsDataMartModel):
    name = models.CharField(max_length=150, null=True, blank=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # unfunded_cash = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    no_units = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=150, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    activity = models.CharField(max_length=150, blank=True, null=True)
    activity_details = models.TextField(blank=True, null=True)
    activity_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    activity_cso_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # activity_unfunded_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    activity_code = models.CharField(max_length=50, blank=True, null=True)

    # LL
    ll_name = models.CharField(max_length=500, blank=True, null=True)
    ll_code = models.CharField(max_length=50, blank=True, null=True)

    loader = InterventionActivityLoader()

    class Meta:
        verbose_name = "Intervention Activity"

    class Options:
        source = ReportsInterventionactivityitem
        depends = (Intervention,)
        mapping = dict(
            pd_number="activity.result.result_link.intervention.number",
            pd_title="activity.result.result_link.intervention.title",
            partner="activity.result.result_link.intervention.agreement.partner.organization.name",
            partner_cso_type="activity.result.result_link.intervention.agreement.partner.organization.cso_type",
            partner_type="activity.result.result_link.intervention.agreement.partner.organization.organization_type",
            partner_vendor_number="activity.result.result_link.intervention.agreement.partner.organization.vendor_number",
            activity="activity.name",
            activity_details="activity.context_details",
            activity_unicef_cash="activity.unicef_cash",
            activity_cso_cash="activity.cso_cash",
            # activity_unfunded_cash="activity.unfunded_cash",
            activity_code="activity.code",
            ll_name="activity.result.name",
            ll_code="activity.result.code",
        )
        queryset = lambda: ReportsInterventionactivityitem.objects.select_related(
            "activity__result__result_link__intervention__agreement__partner__organization"
        )

    # ReportsInterventionactivity ** LL, CP, INT, PART
    # ReportsInterventionactivityTimeFrames **
    # ReportsInterventionactivityitem
    # ReportsInterventiontimeframe
