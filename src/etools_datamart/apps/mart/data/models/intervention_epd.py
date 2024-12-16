import logging

from django.db import models

from etools_datamart.apps.sources.etools.models import PartnersIntervention

from ..loader import EtoolsLoader
from .base import EtoolsDataMartModel
from .intervention import Intervention, InterventionLoader

logger = logging.getLogger(__name__)


class InterventionSimpleAbstract(models.Model):
    pd_number = models.CharField(max_length=64, blank=True, null=True)
    pd_title = models.CharField(max_length=306, null=True, db_index=True)

    # PARTNER
    partner = models.CharField(max_length=255, blank=True, null=True)
    partner_cso_type = models.CharField(max_length=300, blank=True, null=True)
    partner_type = models.CharField(max_length=50, blank=True, null=True)
    partner_vendor_number = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True

    class Options:
        depends = (Intervention,)
        mapping = dict(
            pd_number="number",
            pd_title="title",
            partner="agreement.partner.organization.name",
            partner_cso_type="agreement.partner.organization.cso_type",
            partner_type="agreement.partner.organization.organization_type",
            partner_vendor_number="agreement.partner.organization.vendor_number",
        )


class InterventionEPDLoader(EtoolsLoader):
    pass
    """
    --  
    SET search_path = public,##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "partners_intervention";

    --
    SELECT 'afghanistan' AS __schema, 
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
           "partners_intervention"."context",                           -- directly mapped 
           "partners_intervention"."date_sent_to_partner",              -- directly mapped    
           "partners_intervention"."equity_narrative",                  -- directly mapped   
           "partners_intervention"."equity_rating",                     -- directly mapped   
           "partners_intervention"."gender_narrative",                  -- directly mapped    
           "partners_intervention"."gender_rating",                     -- directly mapped  
           "partners_intervention"."hq_support_cost",                   -- directly mapped 
           "partners_intervention"."implementation_strategy",           -- directly mapped  
           "partners_intervention"."ip_program_contribution",           -- directly mapped
           "partners_intervention"."partner_accepted",                  -- directly mapped
           "partners_intervention"."sustainability_narrative",          -- directly mapped  
           "partners_intervention"."sustainability_rating",             -- directly mapped 
           "partners_intervention"."unicef_accepted",                   -- directly mapped    
           "partners_intervention"."unicef_court",                      -- directly mapped   
           "partners_intervention"."unicef_review_type",                -- directly mapped 
           "partners_intervention"."humanitarian_flag",                 -- directly mapped  
           "partners_intervention"."capacity_development",              -- directly mapped 
           "partners_intervention"."other_info",                        -- directly mapped  
           "partners_intervention"."other_partners_involved",           -- directly mapped  
           "partners_intervention"."technical_guidance",                -- directly mapped 
           "partners_intervention"."cash_transfer_modalities",          -- directly mapped 
           "partners_intervention"."cancel_justification",              -- directly mapped   
           "partners_intervention"."date_partnership_review_performed", -- directly mapped 
           "partners_intervention"."accepted_on_behalf_of_partner",     -- directly mapped  
           "partners_intervention"."activation_protocol",               -- directly mapped  
           "partners_intervention"."confidential",                      -- directly mapped 
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
           "partners_partnerorganization"."organization_id" ,

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

           "auth_user"."id",
           "auth_user"."username"                                      -- directly mapped to .budget_owner 

    FROM "partners_intervention",
    INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_intervention"."agreement_id")
    INNER JOIN "partners_partnerorganization" ON ("partners_partnerorganization"."id" =  "partners_agreement"."partner_id") 
    INNER JOIN "organizations_organization" ON ("organizations_organization"."id" = "partners_partnerorganization"."organization_id")
    INNER JOIN "auth_user" ON ( "auth_user"."id" = "partners_intervention"."budget_owner_id" )
    ORDER BY "partners_intervention"."id" ASC 
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##; 
    """


class InterventionEPD(InterventionSimpleAbstract, EtoolsDataMartModel):
    budget_owner = models.CharField(max_length=150, blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    date_sent_to_partner = models.DateField(blank=True, null=True)
    equity_narrative = models.TextField(blank=True, null=True)
    equity_rating = models.CharField(max_length=50, blank=True, null=True)
    gender_narrative = models.TextField(blank=True, null=True)
    gender_rating = models.CharField(max_length=50, blank=True, null=True)
    hq_support_cost = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    implementation_strategy = models.TextField(blank=True, null=True)
    ip_program_contribution = models.TextField(blank=True, null=True)
    partner_accepted = models.BooleanField(null=True)
    sustainability_narrative = models.TextField(blank=True, null=True)
    sustainability_rating = models.CharField(max_length=50, blank=True, null=True)
    unicef_accepted = models.BooleanField(null=True)
    unicef_court = models.BooleanField(null=True)
    unicef_review_type = models.CharField(max_length=50, blank=True, null=True)
    humanitarian_flag = models.BooleanField(null=True)
    capacity_development = models.TextField(blank=True, null=True)
    other_info = models.TextField(blank=True, null=True)
    other_partners_involved = models.TextField(blank=True, null=True)
    technical_guidance = models.TextField(blank=True, null=True)
    cash_transfer_modalities = models.TextField(blank=True, null=True)  # This field type is a guess.
    cancel_justification = models.TextField(blank=True, null=True)
    date_partnership_review_performed = models.DateField(blank=True, null=True)
    accepted_on_behalf_of_partner = models.BooleanField(null=True)
    activation_protocol = models.TextField(blank=True, null=True)
    confidential = models.BooleanField(null=True)

    loader = InterventionEPDLoader()

    class Meta:
        ordering = ("country_name", "pd_title")
        verbose_name = "Intervention ePD"

    class Options:
        source = PartnersIntervention
        queryset = lambda: PartnersIntervention.objects.all()
        mapping = dict(
            **InterventionSimpleAbstract.Options.mapping,
            budget_owner="budget_owner.username",
        )
