# PartnersInterventionmanagementbudget
# PartnersInterventionmanagementbudgetitem
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import (
    PartnersInterventionmanagementbudget,
    PartnersInterventionmanagementbudgetitem,
)


class InterventionManagementBudgetLoader(EtoolsLoader):
    pass

    """
    --
    SET search_path = public,##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "partners_interventionmanagementbudgetitem";

    --
    SELECT '##COUNTRY##' AS __schema, 
           "partners_interventionmanagementbudgetitem"."id",              -- directly mapped to source_id
           "partners_interventionmanagementbudgetitem"."name",
           "partners_interventionmanagementbudgetitem"."kind",
           "partners_interventionmanagementbudgetitem"."unicef_cash",     -- directly mapped to .unicef_cash
           "partners_interventionmanagementbudgetitem"."cso_cash",        -- directly mapped to .cso_cash  
           "partners_interventionmanagementbudgetitem"."budget_id",   
           "partners_interventionmanagementbudgetitem"."no_units",        -- directly mapped to .no_unit   
           "partners_interventionmanagementbudgetitem"."unit",            -- directly mapped to .unit  
           "partners_interventionmanagementbudgetitem"."unit_price",      -- directly mapped to .unit_price   
           
           "partners_interventionmanagementbudget"."id",
           "partners_interventionmanagementbudget"."created",              -- directly mapped to .budget_created  
           "partners_interventionmanagementbudget"."modified",             -- directly mapped to .budget_modified  
           "partners_interventionmanagementbudget"."act1_unicef",          -- directly mapped to .act1_unicef  
           "partners_interventionmanagementbudget"."act1_partner",         -- directly mapped to .act1_partner 
           "partners_interventionmanagementbudget"."act2_unicef",          -- directly mapped to .act2_unicef
           "partners_interventionmanagementbudget"."act2_partner",         -- directly mapped to .act2_partner
           "partners_interventionmanagementbudget"."act3_unicef",          -- directly mapped to .act3_unicef
           "partners_interventionmanagementbudget"."act3_partner",         -- directly mapped to .act3_partner
           "partners_interventionmanagementbudget"."intervention_id",
           
           "partners_intervention"."id",
           "partners_intervention"."created",
           "partners_intervention"."modified",
           "partners_intervention"."document_type",
           "partners_intervention"."number",                              -- directly mapped to .pd_number   
           "partners_intervention"."title",                               -- directly mapped to .pd_title 
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
    FROM "partners_interventionmanagementbudgetitem" 
    INNER JOIN "partners_interventionmanagementbudget" ON ("partners_interventionmanagementbudgetitem"."budget_id" = "partners_interventionmanagementbudget"."id") 
    INNER JOIN "partners_intervention" ON ("partners_interventionmanagementbudget"."intervention_id" = "partners_intervention"."id") 
    ORDER BY "partners_interventionmanagementbudgetitem"."id" ASC 
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;  


    --
    SELECT 'argentina' AS __schema, 
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
           "partners_agreement"."partner_manager_id" 
    FROM "partners_agreement" WHERE "partners_agreement"."id" IN (##List of "partners_intervention"."agreement_id" in the page ##);

    --
    SELECT 'argentina' AS __schema, 
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
    WHERE "partners_partnerorganization"."id" IN (## LIST of "partners_agreement"."partner_id" in the page ##); 

    -- 
    SELECT "organizations_organization"."id",
           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",                    -- directly mapped to .partner 
           "organizations_organization"."vendor_number",           -- directly mapped to .partner_vendor_number
           "organizations_organization"."organization_type",       -- directly mapped to .partner_type   
           "organizations_organization"."cso_type",                -- directly mapped to .partner_cso_type     
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id" 
    FROM "organizations_organization" 
    WHERE "organizations_organization"."id" IN (## LIST of "partners_partnerorganization"."organization_id" in the page ##); 
    """


class InterventionManagementBudget(InterventionSimpleAbstract, EtoolsDataMartModel):
    # management budget fields
    budget_created = models.DateTimeField()
    budget_modified = models.DateTimeField()
    act1_unicef = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act1_partner = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # act1_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act2_unicef = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act2_partner = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # act2_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act3_unicef = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act3_partner = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # act3_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # management budget item fields
    name = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=15, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # unfunded_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    no_units = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=150, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    loader = InterventionManagementBudgetLoader()

    class Options:
        source = PartnersInterventionmanagementbudgetitem
        depends = (Intervention,)
        mapping = dict(
            pd_number="budget.intervention.number",
            pd_title="budget.intervention.title",
            partner="budget.intervention.agreement.partner.organization.name",
            partner_cso_type="budget.intervention.agreement.partner.organization.cso_type",
            partner_type="budget.intervention.agreement.partner.organization.organization_type",
            partner_vendor_number="budget.intervention.agreement.partner.organization.vendor_number",
            # budget fields
            budget_created="budget.created",
            budget_modified="budget.modified",
            act1_unicef="budget.act1_unicef",
            act1_partner="budget.act1_partner",
            # act1_unfunded="budget.act1_unfunded",
            act2_unicef="budget.act2_unicef",
            act2_partner="budget.act2_partner",
            # act2_unfunded="budget.act2_unfunded",
            act3_unicef="budget.act3_unicef",
            act3_partner="budget.act3_partner",
            # act3_unfunded="budget.act3_unfunded",
        )
        queryset = lambda: PartnersInterventionmanagementbudgetitem.objects.select_related(
            "budget", "budget__intervention"
        )
