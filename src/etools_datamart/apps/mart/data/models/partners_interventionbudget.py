from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import JSONField, Prefetch

from celery.utils.log import get_task_logger

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.models import Location
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention import InterventionAbstract, InterventionLoader
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst, TravelType
from etools_datamart.apps.sources.etools.models import (
    AuthUser,
    DjangoContentType,
    FundsFundsreservationheader,
    LocationsLocation,
    models,
    PartnersFiletype,
    PartnersIntervention,
    PartnersInterventionamendment,
    PartnersInterventionattachment,
    PartnersInterventionbudget,
    PartnersInterventionFlatLocations,
    PartnersInterventionOffices,
    PartnersInterventionPartnerFocalPoints,
    PartnersInterventionplannedvisits,
    PartnersInterventionresultlink,
    PartnersInterventionSections,
    PartnersInterventionUnicefFocalPoints,
    PartnersPartnerorganization,
    ReportsAppliedindicator,
    ReportsLowerresult,
    ReportsOffice,
    ReportsResult,
    ReportsSector,
    T2FTravelactivity,
    UsersUserprofile,
)

logger = get_task_logger(__name__)


class InterventionBudgetLoader(InterventionLoader):
    """
    --
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "partners_interventionbudget" WHERE NOT ("partners_interventionbudget"."intervention_id" IS NULL);

    --
    SELECT 'afghanistan' AS __schema,
           "partners_interventionbudget"."id",
           "partners_interventionbudget"."created",                            -- mapped to created
           "partners_interventionbudget"."modified",                           -- mapped to modified
           "partners_interventionbudget"."partner_contribution",
           "partners_interventionbudget"."unicef_cash",
           "partners_interventionbudget"."in_kind_amount",
           "partners_interventionbudget"."partner_contribution_local",         -- mapped to budget_cso_contribution
           "partners_interventionbudget"."unicef_cash_local",                  -- mapped to budget_unicef_cash
           "partners_interventionbudget"."in_kind_amount_local",               -- mapped to budget_unicef_supply
           "partners_interventionbudget"."total",
           "partners_interventionbudget"."intervention_id",
           "partners_interventionbudget"."total_local",                        -- mapped to budget_total
           "partners_interventionbudget"."currency",                           -- mapped to budget_currency
           "partners_interventionbudget"."programme_effectiveness",
           "partners_interventionbudget"."total_hq_cash_local",
           "partners_interventionbudget"."total_unicef_cash_local_wo_hq",
           "partners_interventionbudget"."partner_supply_local",
           "partners_interventionbudget"."total_partner_contribution_local",

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
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id",

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
           "auth_user"."preferences",

           "reports_countryprogramme"."id",
           "reports_countryprogramme"."name",
           "reports_countryprogramme"."wbs",
           "reports_countryprogramme"."from_date",
           "reports_countryprogramme"."to_date",
           "reports_countryprogramme"."invalid",

           T8."id",
           T8."password",
           T8."last_login",
           T8."is_superuser",
           T8."username",
           T8."first_name",
           T8."last_name",
           T8."email",
           T8."is_staff",
           T8."is_active",
           T8."date_joined",
           T8."middle_name",
           T8."created",
           T8."modified",
           T8."preferences"
    FROM "partners_interventionbudget"
    INNER JOIN "partners_intervention" ON ("partners_interventionbudget"."intervention_id" = "partners_intervention"."id")
    INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_agreement"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    LEFT OUTER JOIN "auth_user" ON ("partners_intervention"."unicef_signatory_id" = "auth_user"."id")
    LEFT OUTER JOIN "reports_countryprogramme" ON ("partners_intervention"."country_programme_id" = "reports_countryprogramme"."id")
    LEFT OUTER JOIN "auth_user" T8 ON ("partners_intervention"."partner_authorized_officer_signatory_id" = T8."id")
    WHERE NOT ("partners_interventionbudget"."intervention_id" IS NULL)
    ORDER BY "partners_interventionbudget"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;


    fr_number=fr.fr_number,
                    vendor_code=fr.vendor_code,
                    fr_type=fr.fr_type,
                    currency=fr.currency,
    --
    SELECT '##COUNTRY##' AS __schema,
           "funds_fundsreservationheader"."id",
           "funds_fundsreservationheader"."vendor_code",    --  part of list of dictionary named fr_numbers_data (fr_number:, vendor_code,: fr_type:, currency:) per partners_intervention"."id"
           "funds_fundsreservationheader"."fr_number",      --  part of list of dictionary named fr_numbers_data (fr_number:, vendor_code,: fr_type:, currency:) per partners_intervention"."id"
                                                            --  comma separated list of named fr_numbers  per partners_intervention"."id"

           "funds_fundsreservationheader"."document_date",
           "funds_fundsreservationheader"."fr_type",        --  part of list of dictionary named fr_numbers_data (fr_number:, vendor_code,: fr_type:, currency:) per partners_intervention"."id"
           "funds_fundsreservationheader"."currency",       --  part of list of dictionary named fr_numbers_data (fr_number:, vendor_code,: fr_type:, currency:) per partners_intervention"."id"
           "funds_fundsreservationheader"."document_text",
           "funds_fundsreservationheader"."start_date",
           "funds_fundsreservationheader"."end_date",
           "funds_fundsreservationheader"."actual_amt",
           "funds_fundsreservationheader"."intervention_id",
           "funds_fundsreservationheader"."intervention_amt",
           "funds_fundsreservationheader"."outstanding_amt",
           "funds_fundsreservationheader"."total_amt",
           "funds_fundsreservationheader"."created",
           "funds_fundsreservationheader"."modified",
           "funds_fundsreservationheader"."actual_amt_local",
           "funds_fundsreservationheader"."outstanding_amt_local",
           "funds_fundsreservationheader"."total_amt_local",
           "funds_fundsreservationheader"."multi_curr_flag",
           "funds_fundsreservationheader"."completed_flag",
           "funds_fundsreservationheader"."delegated"
    FROM "funds_fundsreservationheader"
    WHERE "funds_fundsreservationheader"."intervention_id" IN ( ## List of "partners_intervention"."id" in the page## );

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_interventionamendment"."id",
           "partners_interventionamendment"."created",
           "partners_interventionamendment"."modified",
           "partners_interventionamendment"."signed_date",
           "partners_interventionamendment"."amendment_number",
           "partners_interventionamendment"."signed_amendment",
           "partners_interventionamendment"."intervention_id",
           "partners_interventionamendment"."types",
           "partners_interventionamendment"."other_description",
           "partners_interventionamendment"."amended_intervention_id",
           "partners_interventionamendment"."difference",
           "partners_interventionamendment"."is_active",
           "partners_interventionamendment"."kind",
           "partners_interventionamendment"."related_objects_map",
           "partners_interventionamendment"."signed_by_partner_date",
           "partners_interventionamendment"."signed_by_unicef_date",
           "partners_interventionamendment"."unicef_signatory_id",
           "partners_interventionamendment"."partner_authorized_officer_signatory_id"
    FROM "partners_interventionamendment"
    WHERE "partners_interventionamendment"."intervention_id"  IN ( ## List of "partners_intervention"."id" in the page## );

    --
    SELECT "partners_interventionattachment"."id",
           "partners_interventionattachment"."intervention_id",
           "partners_interventionattachment"."type_id"
    FROM "partners_interventionattachment"
    WHERE "partners_interventionattachment"."intervention_id" IN (## List of "partners_intervention"."id" in the page## );

    --
    SELECT "partners_filetype"."id",
           "partners_filetype"."name"
    FROM "partners_filetype"
    WHERE "partners_filetype"."id" IN (## List of ##);

    --
    SELECT 'afghanistan' AS __schema,
           "partners_interventionplannedvisits"."id",
           "partners_interventionplannedvisits"."year",
           "partners_interventionplannedvisits"."programmatic_q4",
           "partners_interventionplannedvisits"."intervention_id",
           "partners_interventionplannedvisits"."created",
           "partners_interventionplannedvisits"."modified",
           "partners_interventionplannedvisits"."programmatic_q1",
           "partners_interventionplannedvisits"."programmatic_q2",
           "partners_interventionplannedvisits"."programmatic_q3"
    FROM "partners_interventionplannedvisits"
    WHERE ("partners_interventionplannedvisits"."year" = 2025
    AND "partners_interventionplannedvisits"."intervention_id" IN (## List of "partners_intervention"."id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_interventionresultlink"."id",
           "partners_interventionresultlink"."cp_output_id",
           "partners_interventionresultlink"."intervention_id",
           "partners_interventionresultlink"."created",
           "partners_interventionresultlink"."modified",
           "partners_interventionresultlink"."code"
    FROM "partners_interventionresultlink"
    WHERE "partners_interventionresultlink"."intervention_id" IN (## List of "partners_intervention"."id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "reports_lowerresult"."id",
           "reports_lowerresult"."name",
           "reports_lowerresult"."code",
           "reports_lowerresult"."result_link_id",
           "reports_lowerresult"."created",
           "reports_lowerresult"."modified",
           "reports_lowerresult"."is_active"
    FROM "reports_lowerresult"
    WHERE "reports_lowerresult"."result_link_id" IN (## List of  "partners_interventionresultlink"."id" in the page##);

    --
    SELECT 'albania' AS __schema,
           "reports_appliedindicator"."id",
           "reports_appliedindicator"."context_code",
           "reports_appliedindicator"."assumptions",
           "reports_appliedindicator"."total",
           "reports_appliedindicator"."indicator_id",
           "reports_appliedindicator"."lower_result_id",
           "reports_appliedindicator"."means_of_verification",
           "reports_appliedindicator"."cluster_indicator_id",
           "reports_appliedindicator"."cluster_indicator_title",
           "reports_appliedindicator"."cluster_name",
           "reports_appliedindicator"."created",
           "reports_appliedindicator"."modified",
           "reports_appliedindicator"."response_plan_name",
           "reports_appliedindicator"."section_id",
           "reports_appliedindicator"."is_active",
           "reports_appliedindicator"."is_high_frequency",
           "reports_appliedindicator"."baseline",
           "reports_appliedindicator"."denominator_label",
           "reports_appliedindicator"."label",
           "reports_appliedindicator"."measurement_specifications",
           "reports_appliedindicator"."numerator_label",
           "reports_appliedindicator"."target"
    FROM "reports_appliedindicator"
    WHERE "reports_appliedindicator"."lower_result_id" IN (##List of "reports_lowerresult"."id"  in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "t2f_travelactivity"."id",
           "t2f_travelactivity"."travel_type",
           "t2f_travelactivity"."date",
           "t2f_travelactivity"."partner_id",
           "t2f_travelactivity"."partnership_id",
           "t2f_travelactivity"."primary_traveler_id",
           "t2f_travelactivity"."result_id"
    FROM "t2f_travelactivity"
    INNER JOIN "t2f_travelactivity_travels" ON ("t2f_travelactivity"."id" = "t2f_travelactivity_travels"."travelactivity_id")
    INNER JOIN "t2f_travel" ON ("t2f_travelactivity_travels"."travel_id" = "t2f_travel"."id")
    WHERE ("t2f_travelactivity"."date" IS NOT NULL
    AND "t2f_travelactivity"."travel_type" = 'Programmatic Visit' AND "t2f_travel"."status" = 'completed'
    AND "t2f_travelactivity"."partnership_id" IN (##List of "reports_lowerresult"."id"  in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "reports_result"."id",
           "reports_result"."name",
           "reports_result"."code",
           "reports_result"."result_type_id",
           "reports_result"."sector_id",
           "reports_result"."gic_code",
           "reports_result"."gic_name",
           "reports_result"."humanitarian_tag",
           "reports_result"."level",
           "reports_result"."lft",
           "reports_result"."parent_id",
           "reports_result"."rght",
           "reports_result"."sic_code",
           "reports_result"."sic_name",
           "reports_result"."tree_id",
           "reports_result"."vision_id",
           "reports_result"."wbs",
           reports_result"."activity_focus_code",
           "reports_result"."activity_focus_name",
           "reports_result"."hidden",
           "reports_result"."from_date",
           "reports_result"."to_date",
           "reports_result"."ram",
           "reports_result"."country_programme_id",
           "reports_result"."created",
           "reports_result"."modified",
           "reports_result"."humanitarian_marker_code",
           "reports_result"."humanitarian_marker_name",
           "reports_result"."programme_area_code",
           "reports_result"."programme_area_name"
    FROM "reports_result"
    WHERE "reports_result"."country_programme_id" IN (##List of  "reports_countryprogramme"."id" un the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_intervention_sections"."id",
           "partners_intervention_sections"."intervention_id",
           "partners_intervention_sections"."section_id"
    FROM "partners_intervention_sections"
    WHERE "partners_intervention_sections"."intervention_id" IN (## List of "partners_intervention"."id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "reports_sector"."id",
           "reports_sector"."name",
           "reports_sector"."description",
           "reports_sector"."alternate_id",
           "reports_sector"."alternate_name",
           "reports_sector"."dashboard",
           "reports_sector"."color",
           "reports_sector"."created",
           "reports_sector"."modified",
           "reports_sector"."active"
    FROM "reports_sector" WHERE "reports_sector"."id" IN (## List of  "reports_result"."sector_id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_intervention_offices"."id",
           "partners_intervention_offices"."intervention_id",
           "partners_intervention_offices"."office_id"
    FROM "partners_intervention_offices"
    WHERE "partners_intervention_offices"."intervention_id" IN (##List of "partners_intervention"."id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "reports_office"."id",
           "reports_office"."name"
    FROM "reports_office"
    WHERE "reports_office"."id" IN (##List of "partners_intervention_offices"."id" in the page##)
    ORDER BY "reports_office"."id" ASC;

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_intervention_unicef_focal_points"."id",
           "partners_intervention_unicef_focal_points"."intervention_id",
           "partners_intervention_unicef_focal_points"."user_id"
    FROM "partners_intervention_unicef_focal_points"
    WHERE "partners_intervention_unicef_focal_points"."intervention_id" IN (## List of "partners_intervention"."id" in the page##);

    --
    SELECT "auth_user"."id",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email"
    FROM "auth_user" WHERE "auth_user"."id" IN (##List of partners_intervention_unicef_focal_points"."user_id" in the page##);

    --
    SELECT "partners_intervention_partner_focal_points"."id",
           "partners_intervention_partner_focal_points"."intervention_id",
           "partners_intervention_partner_focal_points"."user_id"
    FROM "partners_intervention_partner_focal_points"
    WHERE "partners_intervention_partner_focal_points"."intervention_id" IN (## List of "partners_intervention"."id" in the page##);

    --
    SELECT "auth_user"."id",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email"
    FROM "auth_user"
    WHERE "auth_user"."id" IN (##List of "partners_intervention_partner_focal_points"."user_id" in the page##);

    --
    SELECT "users_userprofile"."id",
           "users_userprofile"."phone_number",
           "users_userprofile"."user_id"
    FROM "users_userprofile"
    WHERE "users_userprofile"."user_id" IN (## List of "partners_intervention_partner_focal_points"."user_id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_intervention_flat_locations"."id",
           "partners_intervention_flat_locations"."intervention_id",
           "partners_intervention_flat_locations"."location_id"
    FROM "partners_intervention_flat_locations"
    WHERE "partners_intervention_flat_locations"."intervention_id" IN (## List of "partners_intervention"."id" in the page##);

    locations_data = []
        for item in record.PartnersInterventionFlatLocations_intervention.all():
            # TODO: Check possible available json serialization
            loc_data = dict(
                name=item.location.name,
                level=item.location.admin_level,
                pcode=item.location.p_code,
                latitude=item.location.latitude,
                levelname=item.location.admin_level_name,
                longitude=item.location.longitude,
                source_id=item.location.id,
            )
            locations_data.append(loc_data)

        return locations_data

    --
    SELECT "locations_location"."id",
           "locations_location"."name",            -- added to list of dict name locations_data (per "partners_intervention_flat_locations"."id")
                                                   -- forms list of comma separated strinng property with name  locations (per "partners_intervention_flat_locations"."id")

           "locations_location"."latitude",        -- added to list of dict name locations_data (per "partners_intervention_flat_locations"."id")
           "locations_location"."longitude",       -- added to list of dict name locations_data (per "partners_intervention_flat_locations"."id")
           "locations_location"."p_code",          -- added to list of dict name locations_data (per "partners_intervention_flat_locations"."id")
           "locations_location"."admin_level",     -- added to list of dict name locations_data (per "partners_intervention_flat_locations"."id")
           "locations_location"."admin_level_name" -- added to list of dict name locations_data (per "partners_intervention_flat_locations"."id")
    FROM "locations_location"
    WHERE "locations_location"."id" IN (## List of "partners_intervention_flat_locations"."id" in the page ##);

    --
    SELECT "reports_result"."id",
           "reports_result"."name",
           "reports_result"."wbs"
    FROM "reports_result"
    WHERE "reports_result"."id" IN (## ##);

    --
    SELECT "users_country"."id",
           "users_country"."schema_name",
           "users_country"."name",
           "users_country"."business_area_code",
           "users_country"."initial_zoom",
           "users_country"."latitude",
           "users_country"."longitude",
           "users_country"."country_short_code",
           "users_country"."vision_sync_enabled",
           "users_country"."vision_last_synced",
           "users_country"."local_currency_id",
           "users_country"."long_name",
           "users_country"."iso3_code",
           "users_country"."custom_dashboards"
    FROM "users_country"
    WHERE "users_country"."schema_name" = '##COUNTRY##';

    """

    def get_queryset(self):
        return (
            PartnersInterventionbudget.objects.exclude(intervention__isnull=True)
            .select_related(
                "intervention",
                "intervention__unicef_signatory",
                "intervention__agreement",
                "intervention__agreement__partner",
                "intervention__agreement__partner__organization",
                "intervention__country_programme",
                "intervention__partner_authorized_officer_signatory",
            )
            .prefetch_related(
                Prefetch(
                    "intervention__FundsFundsreservationheader_intervention",
                    queryset=FundsFundsreservationheader.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionamendment_intervention",
                    queryset=PartnersInterventionamendment.objects.all().order_by("signed_date"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionattachment_intervention",
                    queryset=PartnersInterventionattachment.objects.all().only(
                        "id",
                        "intervention_id",
                        "type_id",
                    ),
                ),
                Prefetch(
                    "intervention__PartnersInterventionattachment_intervention__type",
                    queryset=PartnersFiletype.objects.all().only(
                        "id",
                        "name",
                    ),
                ),
                Prefetch(
                    "intervention__PartnersInterventionplannedvisits_intervention",
                    queryset=PartnersInterventionplannedvisits.objects.filter(year=self.context["today"].year),
                ),
                Prefetch(
                    "intervention__PartnersInterventionresultlink_intervention__ReportsLowerresult_result_link__ReportsAppliedindicator_lower_result",
                    queryset=ReportsAppliedindicator.objects.all(),
                ),
                Prefetch(
                    "intervention__T2FTravelactivity_partnership",
                    queryset=T2FTravelactivity.objects.filter(
                        travel_type=TravelType.PROGRAMME_MONITORING,
                        travels__status="completed",
                        date__isnull=False,
                    ).order_by("date"),
                ),
                Prefetch(
                    "intervention__country_programme__ReportsResult_country_programme",
                    queryset=ReportsResult.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionSections_intervention",
                    queryset=PartnersInterventionSections.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionSections_intervention__section",
                    queryset=ReportsSector.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionOffices_intervention__office",
                    queryset=ReportsOffice.objects.all().order_by("id"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionUnicefFocalPoints_intervention",
                    queryset=PartnersInterventionUnicefFocalPoints.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionUnicefFocalPoints_intervention__user",
                    queryset=AuthUser.objects.only("id", "username", "first_name", "last_name", "email"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionPartnerFocalPoints_intervention",
                    queryset=PartnersInterventionPartnerFocalPoints.objects.only("id", "intervention_id", "user_id"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionPartnerFocalPoints_intervention__user",
                    queryset=AuthUser.objects.only("id", "username", "first_name", "last_name", "email", "profile"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionPartnerFocalPoints_intervention__user__profile",
                    queryset=UsersUserprofile.objects.only("id", "phone_number", "user_id"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionFlatLocations_intervention",
                    queryset=PartnersInterventionFlatLocations.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionFlatLocations_intervention__location",
                    queryset=LocationsLocation.objects.only(
                        "id",
                        "name",
                        "admin_level",
                        "p_code",
                        "latitude",
                        "admin_level_name",
                        "longitude",
                    ),
                ),
                Prefetch(
                    "intervention__PartnersInterventionresultlink_intervention__cp_output",
                    queryset=ReportsResult.objects.only("id", "name", "wbs"),
                ),
            )
        )

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")
        qs = self.get_queryset()

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                filters = self.config.key(self, record)
                values = self.get_values(record.intervention)
                values["source_id"] = record.id
                values["budget_cso_contribution"] = record.partner_contribution_local
                values["budget_unicef_cash"] = record.unicef_cash_local
                # values["budget_total_unfunded"] = record.total_unfunded
                values["budget_total"] = record.total_local
                values["budget_currency"] = record.currency
                values["budget_unicef_supply"] = record.in_kind_amount_local
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def get_fr_numbers(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        ret = []

        for fr in record.FundsFundsreservationheader_intervention.all():
            ret.append(fr.fr_number)
            data.append(
                dict(
                    fr_number=fr.fr_number,
                    vendor_code=fr.vendor_code,
                    fr_type=fr.fr_type,
                    currency=fr.currency,
                )
            )

        values["fr_numbers_data"] = data
        return ", ".join(ret)


class InterventionBudget(InterventionAbstract, EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    budget_cso_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=5, blank=True, null=True)
    budget_total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # budget_total_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_supply = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fr_numbers = models.TextField(max_length=100, blank=True, null=True)
    fr_numbers_data = JSONField(blank=True, null=True, default=dict)

    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionBudgetLoader()

    class Meta:
        ordering = ("-created",)

    class Options(InterventionAbstract.Options):
        model = PartnersInterventionbudget
        depends = (Location,)
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, source_id=record.pk)
