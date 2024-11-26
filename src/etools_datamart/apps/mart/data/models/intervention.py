import datetime
import logging

from django.conf import settings
from django.core.paginator import Paginator
from django.db import models, transaction
from django.db.models import F, JSONField, Prefetch, Q, Subquery, Sum
from django.utils.functional import cached_property

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.reports_office import Office
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst, TravelType
from etools_datamart.apps.sources.etools.models import (
    AuthUser,
    DjangoContentType,
    FundsFundsreservationheader,
    LocationsLocation,
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
    PartnersInterventionreview,
    PartnersInterventionSections,
    PartnersInterventionUnicefFocalPoints,
    ReportsAppliedindicator,
    ReportsLowerresult,
    ReportsOffice,
    ReportsResult,
    ReportsSector,
    T2FTravelactivity,
    UsersUserprofile,
)

from .base import EtoolsDataMartModel
from .location import Location
from .mixins import add_location_mapping, LocationMixin, NestedLocationLoaderMixin, NestedLocationMixin
from .partner import Partner

logger = logging.getLogger(__name__)


class InterventionAbstract(models.Model):
    agreement_reference_number = models.CharField(max_length=300, blank=True, null=True)
    amendment_types = models.TextField(blank=True, null=True)
    attachment_types = models.TextField(blank=True, null=True)
    agreement_id = models.IntegerField(blank=True, null=True)
    cfei_number = models.CharField(max_length=150, null=True, blank=True)
    clusters = models.TextField(blank=True, null=True)
    contingency_pd = models.BooleanField(null=True)
    cp_outputs = models.TextField(blank=True, null=True)
    cp_outputs_data = JSONField(blank=True, null=True, default=dict)

    cso_type = models.CharField(max_length=300, blank=True, null=True)
    country_programme = models.CharField(max_length=300, blank=True, null=True)
    country_programme_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)
    days_from_prc_review_to_signature = models.IntegerField(blank=True, null=True)
    days_from_submission_to_signature = models.IntegerField(blank=True, null=True)
    document_type = models.CharField(max_length=255, null=True, choices=PartnersInterventionConst.INTERVENTION_TYPES)
    end_date = models.DateField(null=True)
    fr_number = models.CharField(max_length=300, blank=True, null=True)
    outstanding_amt_local = models.DecimalField(default=0, max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    intervention_id = models.IntegerField(blank=True, null=True)
    last_amendment_date = models.DateField(blank=True, null=True)
    metadata = JSONField(blank=True, null=True, default=dict)
    number = models.CharField(max_length=64, null=True)
    number_of_attachments = models.IntegerField(blank=True, null=True)
    number_of_amendments = models.IntegerField(blank=True, null=True)
    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)
    partner_authorized_officer_signatory_id = models.IntegerField(null=True)
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_focal_points = models.TextField(blank=True, null=True)
    partner_focal_points_data = JSONField(blank=True, null=True, default=dict)
    # partner_focal_point_email = models.CharField(max_length=128, null=True)
    # partner_focal_point_first_name = models.CharField(max_length=64, null=True)
    # partner_focal_point_last_name = models.CharField(max_length=64, null=True)
    # partner_focal_point_phone = models.CharField(max_length=64, null=True)
    # partner_focal_point_title = models.CharField(max_length=64, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=200, null=True)
    partner_sea_risk_rating = models.CharField(max_length=150, null=True, blank=True)
    partner_signatory_name = models.CharField(max_length=300, null=True)
    partner_signatory_email = models.CharField(max_length=128, null=True)
    partner_signatory_first_name = models.CharField(max_length=64, null=True)
    partner_signatory_last_name = models.CharField(max_length=64, null=True)
    partner_signatory_phone = models.CharField(max_length=64, null=True)
    partner_signatory_title = models.CharField(max_length=100, null=True)
    partner_source_id = models.IntegerField(blank=True, null=True)
    partner_type = models.CharField(max_length=64, null=True)
    partner_vendor_number = models.CharField(max_length=100, blank=True, null=True)
    planned_programmatic_visits = models.IntegerField(blank=True, null=True)
    population_focus = models.CharField(max_length=130, null=True)
    prc_review_document = models.CharField(max_length=1024, null=True)
    review_date_prc = models.DateField(null=True)
    reference_number = models.CharField(max_length=100, null=True)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    signed_by_partner_date = models.DateField(null=True)
    signed_by_unicef_date = models.DateField(null=True)
    signed_pd_document = models.CharField(max_length=1024, null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=32, null=True, db_index=True, choices=PartnersInterventionConst.STATUSES)
    submission_date = models.DateField(null=True)
    submission_date_prc = models.DateField(null=True)
    title = models.CharField(max_length=306, null=True, db_index=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # has_unfunded_cash = models.BooleanField(null=True)
    # total_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_focal_points = models.TextField(blank=True, null=True)
    unicef_focal_points_data = JSONField(blank=True, null=True, default=dict)
    unicef_signatory_name = models.CharField(max_length=500, null=True)
    # unicef_signatory_first_name = models.CharField(max_length=30, null=True)
    # unicef_signatory_id = models.IntegerField(blank=True, null=True)
    # unicef_signatory_last_name = models.CharField(max_length=30, null=True)
    updated = models.DateTimeField(null=True)
    last_pv_date = models.DateField(null=True, blank=True)

    has_activities_involving_children = models.BooleanField(null=True)
    has_data_processing_agreement = models.BooleanField(null=True)
    has_special_conditions_for_construction = models.BooleanField(null=True)
    final_review_approved = models.BooleanField(null=True)
    other_details = models.TextField(blank=True, null=True)

    # disbursement_percent = models.IntegerField('Disbursement To Date (%)')

    class Meta:
        abstract = True

    class Options:
        depends = (Office, Location, Partner)
        source = PartnersIntervention
        queryset = lambda: PartnersIntervention.objects.select_related(
            "agreement",
            "partner_authorized_officer_signatory",
            "unicef_signatory",
            "country_programme",
            "partnersintervention_partners_interventionbudget_intervention_id",
        )
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, intervention_id=record.pk)
        mapping = dict(
            agreement_reference_number="agreement.reference_number",
            amendment_types="-",
            attachment_types="-",
            clusters="-",
            contingency_pd="=",
            country_programme="country_programme.name",
            country_programme_id="country_programme.pk",
            cp_outputs="-",
            created="=",
            cso_type="agreement.partner.organization.cso_type",
            currency="PartnersInterventionbudget_intervention.currency",
            days_from_submission_to_signature="-",
            days_from_prc_review_to_signature="-",
            end_date="end",
            fr_number="-",
            outstanding_amt_local="-",
            in_kind_amount="PartnersInterventionbudget_intervention.in_kind_amount",
            in_kind_amount_local="PartnersInterventionbudget_intervention.in_kind_amount_local",
            intervention_id="id",
            last_amendment_date="i",
            last_pv_date="-",
            location="i",
            # locations_data="-",
            # locations="-",
            number_of_amendments="i",
            number_of_attachments="i",
            offices="-",
            offices_data="i",
            partner_authorized_officer_signatory_id="partner_authorized_officer_signatory.pk",
            partner_contribution="PartnersInterventionbudget_intervention.partner_contribution",
            partner_contribution_local="PartnersInterventionbudget_intervention.partner_contribution_local",
            partner_focal_points="-",
            partner_focal_points_data="i",
            partner_id="-",
            partner_name="agreement.partner.organization.name",
            partner_sea_risk_rating="i",
            partner_signatory_email="partner_authorized_officer_signatory.email",
            partner_signatory_first_name="partner_authorized_officer_signatory.first_name",
            partner_signatory_last_name="partner_authorized_officer_signatory.last_name",
            partner_signatory_phone="partner_authorized_officer_signatory.phone",
            partner_signatory_title="partner_authorized_officer_signatory.title",
            partner_source_id="agreement.partner.id",
            partner_type="agreement.partner.organization.organization_type",
            partner_vendor_number="agreement.partner.organization.vendor_number",
            planned_programmatic_visits="-",
            prc_review_document="-",
            sections="-",
            start_date="start",
            status="=",
            total="PartnersInterventionbudget_intervention.total",
            # has_unfunded_cash="PartnersInterventionbudget_intervention.has_unfunded_cash",
            # total_unfunded="PartnersInterventionbudget_intervention.total_unfunded",
            total_local="PartnersInterventionbudget_intervention.total_local",
            unicef_cash="PartnersInterventionbudget_intervention.unicef_cash",
            unicef_cash_local="PartnersInterventionbudget_intervention.unicef_cash_local",
            unicef_focal_points="-",
            unicef_focal_points_data="i",
            # unicef_signatory_email='unicef_signatory.email',
            # unicef_signatory_first_name='unicef_signatory.first_name',
            # unicef_signatory_id='unicef_signatory.pk',
            # unicef_signatory_last_name='unicef_signatory.last_name',
            updated="modified",
            cfei_number="=",
        )


class InterventionLoader(NestedLocationLoaderMixin, EtoolsLoader):
    """
    -- TODO: Pick only the required fields
    SET search_path = public;
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
            "users_country"."custom_dashboards" FROM
            "users_country" WHERE "users_country"."schema_name" = '##COUNTRY##' LIMIT 21

    -- TODO: Pick only the required fields
    SET search_path = public, albania;
    SELECT '##COUNTRY##' AS __schema,
        "partners_intervention"."id",
        "partners_intervention"."created",
        "partners_intervention"."modified",
        "partners_intervention"."document_type",
        "partners_intervention"."number",
        "partners_intervention"."title",
        "partners_intervention"."status",
        "partners_intervention"."start", "partners_intervention"."end", "partners_intervention"."submission_date",
        "partners_intervention"."submission_date_prc", "partners_intervention"."review_date_prc",
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

        "partners_interventionbudget"."id",
        "partners_interventionbudget"."partner_contribution",
        "partners_interventionbudget"."unicef_cash",
        "partners_interventionbudget"."in_kind_amount",
        "partners_interventionbudget"."partner_contribution_local",
        "partners_interventionbudget"."unicef_cash_local",
        "partners_interventionbudget"."in_kind_amount_local",
        "partners_interventionbudget"."total",
        "partners_interventionbudget"."intervention_id",
        "partners_interventionbudget"."total_local",
        "partners_interventionbudget"."currency",

        "partners_interventionamendment"."id",
        "partners_interventionamendment"."signed_date",
        "partners_interventionamendment"."intervention_id",
        "partners_interventionamendment"."types",

        "funds_fundsreservationheader"."id",
        "funds_fundsreservationheader"."fr_number",
        "funds_fundsreservationheader"."intervention_id",
        "funds_fundsreservationheader"."outstanding_amt_local",

        "partners_interventionattachment"."id",
        "partners_interventionattachment"."intervention_id",
        "partners_interventionattachment"."type_id",

        "partners_interventionplannedvisits"."id",
        "partners_interventionplannedvisits"."intervention_id",
        "partners_interventionplannedvisits"."programmatic_q1",
        "partners_interventionplannedvisits"."programmatic_q2",
        "partners_interventionplannedvisits"."programmatic_q3",

        "partners_intervention_unicef_focal_points"."id",
        "partners_intervention_unicef_focal_points"."user_id",

        "partners_intervention_partner_focal_points"."id",
        "partners_intervention_partner_focal_points"."intervention_id",
        "partners_intervention_partner_focal_points"."user_id",

        "partners_intervention_flat_locations"."id",
        "partners_intervention_flat_locations"."intervention_id",
        "partners_intervention_flat_locations"."location_id",

        "locations_location"."id",
        "locations_location"."name",
        "locations_location"."latitude",
        "locations_location"."longitude",
        "locations_location"."p_code",
        "locations_location"."admin_level",
        "locations_location"."admin_level_name"
    FROM "partners_intervention"
    INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_agreement"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    LEFT OUTER JOIN "auth_user" ON ("partners_intervention"."unicef_signatory_id" = "auth_user"."id")
    LEFT OUTER JOIN "reports_countryprogramme" ON ("partners_intervention"."country_programme_id" = "reports_countryprogramme"."id")
    INNER JOIN "partners_interventionbudget"  ON("partners_interventionbudget"."intervention_id" = "partners_intervention"."id")
    INNER JOIN "partners_interventionamendment" ON ("partners_interventionamendment"."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "funds_fundsreservationheader" ON ("funds_fundsreservationheader"."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "partners_interventionattachment" ON ("partners_interventionattachment"."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "partners_interventionplannedvisits" ON ("partners_interventionplannedvisits"."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "partners_intervention_unicef_focal_points" ON ("partners_intervention_unicef_focal_points"."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "partners_intervention_partner_focal_points" ON ("partners_intervention_partner_focal_points" ."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "partners_intervention_flat_locations" ON ("partners_intervention_flat_locations"."intervention_id" = "partners_intervention"."id" )
    INNER JOIN "locations_location" ON ("locations_location"."id" = "partners_intervention_flat_locations"."location_id" )
    ORDER BY "partners_intervention"."id" ASC

    """

    location_m2m_field = "flat_locations"

    def get_queryset(self):
        # TODO: Minimize the number of fields for tables joined with select_related
        return PartnersIntervention.objects.select_related(
            "agreement__partner__organization",
            "unicef_signatory",
            "country_programme",
            "partner_authorized_officer_signatory",
        ).prefetch_related(
            Prefetch(
                "PartnersInterventionbudget_intervention",
                queryset=PartnersInterventionbudget.objects.all().only(
                    "id",
                    "currency",
                    "total",
                    "total_local",
                    "in_kind_amount",
                    "in_kind_amount_local",
                    "intervention_id",
                    "partner_contribution",
                    "partner_contribution_local",
                    "unicef_cash",
                    "unicef_cash_local",
                ),
            ),
            Prefetch(
                "PartnersInterventionamendment_intervention",
                queryset=PartnersInterventionamendment.objects.all()
                .order_by("signed_date")
                .only(
                    "id",
                    "signed_date",
                    "intervention_id",
                    "types",
                ),
            ),
            Prefetch(
                "FundsFundsreservationheader_intervention",
                queryset=FundsFundsreservationheader.objects.all().only(
                    "id",
                    "fr_number",
                    "outstanding_amt_local",
                    "intervention_id",
                ),
            ),
            Prefetch(
                "PartnersInterventionattachment_intervention",
                queryset=PartnersInterventionattachment.objects.all().only(
                    "id",
                    "intervention_id",
                    "type_id",
                ),
            ),
            Prefetch(
                "PartnersInterventionattachment_intervention__type",
                queryset=PartnersFiletype.objects.all().only(
                    "id",
                    "name",
                ),
            ),
            Prefetch(
                "PartnersInterventionplannedvisits_intervention",
                queryset=PartnersInterventionplannedvisits.objects.filter(year=self.context["today"].year).only(
                    "id",
                    "intervention_id",
                    "programmatic_q1",
                    "programmatic_q2",
                    "programmatic_q3",
                ),
            ),
            Prefetch(
                "T2FTravelactivity_partnership",
                queryset=T2FTravelactivity.objects.filter(
                    travel_type=TravelType.PROGRAMME_MONITORING,
                    travels__status="completed",
                    date__isnull=False,
                )
                .order_by("-date")
                .only("id", "date", "travel_type", "partnership_id"),
            ),
            Prefetch(
                "PartnersInterventionresultlink_intervention",
                queryset=PartnersInterventionresultlink.objects.all(),
            ),
            Prefetch(
                "PartnersInterventionresultlink_intervention__ReportsLowerresult_result_link__ReportsAppliedindicator_lower_result",
                queryset=ReportsAppliedindicator.objects.all(),
            ),
            Prefetch(
                "PartnersInterventionSections_intervention",
                queryset=PartnersInterventionSections.objects.all(),
            ),
            Prefetch(
                "PartnersInterventionSections_intervention__section",
                queryset=ReportsSector.objects.only("id", "name", "description"),
            ),
            Prefetch(
                "PartnersInterventionOffices_intervention",
                queryset=PartnersInterventionOffices.objects.all().order_by("id"),
            ),
            Prefetch(
                "PartnersInterventionOffices_intervention__office",
                queryset=ReportsOffice.objects.all().order_by("id", "name"),
            ),
            Prefetch(
                "PartnersInterventionUnicefFocalPoints_intervention",
                queryset=PartnersInterventionUnicefFocalPoints.objects.all(),
            ),
            Prefetch(
                "PartnersInterventionUnicefFocalPoints_intervention__user",
                queryset=AuthUser.objects.only("id", "username", "first_name", "last_name", "email"),
            ),
            Prefetch(
                "PartnersInterventionPartnerFocalPoints_intervention",
                queryset=PartnersInterventionPartnerFocalPoints.objects.only("id", "intervention_id", "user_id"),
            ),
            Prefetch(
                "PartnersInterventionPartnerFocalPoints_intervention__user",
                queryset=AuthUser.objects.only("id", "username", "first_name", "last_name", "email", "profile"),
            ),
            Prefetch(
                "PartnersInterventionPartnerFocalPoints_intervention__user__profile",
                queryset=UsersUserprofile.objects.only("id", "phone_number", "user_id"),
            ),
            Prefetch(
                "PartnersInterventionFlatLocations_intervention",
                queryset=PartnersInterventionFlatLocations.objects.only("id", "intervention_id", "location_id"),
            ),
            Prefetch(
                "PartnersInterventionFlatLocations_intervention__location",
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
                "PartnersInterventionreview_intervention",
                queryset=PartnersInterventionreview.objects.all(),
            ),
            Prefetch(
                "PartnersInterventionresultlink_intervention__cp_output",
                queryset=ReportsResult.objects.only("id", "name", "wbs"),
            ),
        )

    @cached_property
    def _ct(self):
        return DjangoContentType.objects.get(app_label="partners", model="intervention").model

    # def fr_currencies_ok(self, original: PartnersIntervention):
    #     return original.frs__currency__count == 1 if original.frs__currency__count else None

    def get_partner_id(self, record: PartnersIntervention, values: dict, **kwargs):
        try:
            data = Partner.objects.get(
                schema_name=self.context["country"].schema_name,
                source_id=record.agreement.partner.id,
            )
            values["partner_sea_risk_rating"] = data.sea_risk_rating_name
            return data.pk
        except Partner.DoesNotExist:
            values["partner_sea_risk_rating"] = None
            return None

    def get_planned_programmatic_visits(self, record: PartnersIntervention, values: dict, **kwargs):
        # TODO: put extra logic to make it more reliable
        for item in record.PartnersInterventionplannedvisits_intervention.all():
            planned = item.programmatic_q1 + item.programmatic_q2 + item.programmatic_q3
            return planned

    def get_attachment_types(self, record: PartnersIntervention, values: dict, **kwargs):
        count = 0
        types_list = []
        for item in record.PartnersInterventionattachment_intervention.all():
            count = count + 1
            types_list.append(str(item.type.name))

        values["number_of_attachments"] = count

        return ", ".join(types_list)

    def get_amendment_types(self, record: PartnersIntervention, values: dict, **kwargs):
        count = 0
        values["last_amendment_date"] = None
        types_list = []
        for item in record.PartnersInterventionamendment_intervention.all():
            count = count + 1
            values["last_amendment_date"] = item.signed_date
            types_list.append(str(item.types))

        values["number_of_amendments"] = count
        return ", ".join(types_list)

    def get_days_from_prc_review_to_signature(self, record: PartnersIntervention, values: dict, **kwargs):
        i1 = record.review_date_prc
        i2 = record.signed_by_partner_date
        if i1 and i2:
            return (i2 - i1).days

    def get_days_from_submission_to_signature(self, record: PartnersIntervention, values: dict, **kwargs):
        i1 = record.submission_date
        i2 = record.signed_by_unicef_date
        if i1 and i2:
            return (i2 - i1).days

    def get_sections(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        for item in record.PartnersInterventionSections_intervention.all():
            data.append(
                dict(
                    source_id=item.section.id,
                    name=item.section.name,
                    description=item.section.description,
                )
            )
        values["sections_data"] = data
        return ", ".join([sec["name"] for sec in data])

    def get_last_pv_date(self, record: PartnersIntervention, values: dict, **kwargs):
        ta_date = None
        for item in record.T2FTravelactivity_partnership.all():
            return item.date
        return ta_date

    def get_unicef_signatory_name(self, record: PartnersIntervention, values: dict, **kwargs):
        if record.unicef_signatory:
            return "{0.username} ({0.email})".format(record.unicef_signatory)

    def get_partner_signatory_name(self, record: PartnersIntervention, values: dict, **kwargs):
        if record.partner_authorized_officer_signatory:
            return "{0.last_name} {0.first_name} ({0.email})".format(record.partner_authorized_officer_signatory)

    def get_offices(self, record: PartnersIntervention, values: dict, **kwargs):
        # PartnersInterventionOffices
        data = []
        for item in record.PartnersInterventionOffices_intervention.all():
            data.append(
                dict(
                    source_id=item.office.id,
                    name=item.office.name,
                )
            )
        values["offices_data"] = data
        return ", ".join([off["name"] for off in data])

    def get_clusters(self, record: PartnersIntervention, values: dict, **kwargs):
        clusters = set()
        for result_link in record.PartnersInterventionresultlink_intervention.all():
            # print(type(result_link))
            for lower_result in result_link.ReportsLowerresult_result_link.all():
                # print(type(lower_result))
                for applied_indicator in lower_result.ReportsAppliedindicator_lower_result.all():
                    # print(type(applied_indicator))
                    if applied_indicator.cluster_name:
                        clusters.add(applied_indicator.cluster_name)
        return ", ".join(clusters)

    def get_partner_focal_points(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        ret = []
        for member in record.PartnersInterventionPartnerFocalPoints_intervention.all():
            # member is AUTH_USER_MODEL
            ret.append(
                "{0.user.last_name} {0.user.first_name} ({0.user.email}) {0.user.profile.phone_number}".format(member)
            )
            data.append(
                dict(
                    last_name=member.user.last_name,
                    first_name=member.user.first_name,
                    email=member.user.email,
                    phone=member.user.profile.phone_number,
                )
            )

        values["partner_focal_points_data"] = data
        return ", ".join(ret)

    def get_fr_number(self, record: PartnersIntervention, values: dict, **kwargs):
        fr_number_list = []

        for item in record.FundsFundsreservationheader_intervention.all():
            fr_number_list.append(item.fr_number)

        return ", ".join(fr_number_list)

    def get_outstanding_amt_local(self, record: PartnersIntervention, values: dict, **kwargs):
        sum_outstanding_amt_local = 0
        for item in record.FundsFundsreservationheader_intervention.all():
            sum_outstanding_amt_local = sum_outstanding_amt_local + item.outstanding_amt_local

        return sum_outstanding_amt_local

    def get_cp_outputs(self, record: PartnersIntervention, values: dict, **kwargs):
        outputs_data = []
        outputs = []
        for item in record.PartnersInterventionresultlink_intervention.all():
            if item.cp_output:
                outputs_data.append(dict(name=item.cp_output.name, wbs=item.cp_output.wbs))
                outputs.append(item.cp_output.name)
        values["cp_outputs_data"] = outputs_data
        return ", ".join(outputs)

    def get_unicef_focal_points(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        ret = []
        for item in record.PartnersInterventionUnicefFocalPoints_intervention.all():
            ret.append("{0.user.last_name} {0.user.first_name} ({0.user.email})".format(item))
            data.append(
                dict(
                    last_name=item.user.last_name,
                    first_name=item.user.first_name,
                    email=item.user.email,
                )
            )

        values["unicef_focal_points_data"] = data
        return ", ".join(ret)

    def get_prc_review_document(self, record: PartnersIntervention, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Attachment

        attachment = (
            Attachment.objects.filter(
                # object_id=record.pk,
                pd_ssfa_number__in=[record.number, record.number[:-2] if record.number else ""],
                code="partners_intervention_prc_review",
                content_type=self._ct,
            )
            .order_by("-id")
            .first()
        )
        if attachment:
            return attachment.file

    def get_final_partnership_review(self, record: PartnersIntervention, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Attachment

        attachment = Attachment.objects.filter(
            pd_ssfa_number=record.number, code="partners_intervention_attachment", content_type="interventionattachment"
        ).last()
        if attachment:
            return attachment.file

    def get_locations(self, record: PartnersIntervention, values: dict, **kwargs):
        locations = []
        for item in record.PartnersInterventionFlatLocations_intervention.all():
            locations.append(item.location.name)
        return ", ".join(locations)

    def get_locations_data(self, record: PartnersIntervention, values: dict, **kwargs):
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


class Intervention(NestedLocationMixin, InterventionAbstract, EtoolsDataMartModel):
    final_partnership_review = models.CharField(max_length=1024, null=True)

    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionLoader()

    class Meta:
        ordering = ("country_name", "title", "id")
        verbose_name = "Intervention"
        unique_together = ("schema_name", "intervention_id")

    class Options(InterventionAbstract.Options):
        mapping = dict(
            **InterventionAbstract.Options.mapping,
            locations_data="-",
            locations="-",
            final_partnership_review="-",
        )


class InterventionByLocationLoader(InterventionLoader):
    def get_values(self, record):
        values = super().get_values(record)
        values["location"] = Location.objects.filter(
            schema_name=self.context["country"].schema_name, source_id=record.location.id
        ).first()
        return values

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.filter_queryset(self.get_queryset().prefetch_related("flat_locations"))

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for intervention in page.object_list:
                for location in intervention.flat_locations.all():
                    intervention.location = location
                    filters = self.config.key(self, intervention)
                    values = self.get_values(intervention)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)


class InterventionByLocation(LocationMixin, InterventionAbstract, EtoolsDataMartModel):
    loader = InterventionByLocationLoader()

    class Meta:
        ordering = ("country_name", "title")
        verbose_name = "Intervention By Location"
        unique_together = ("schema_name", "intervention_id", "location_source_id")

    class Options(InterventionAbstract.Options):
        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name,
            intervention_id=record.pk,
            location_source_id=record.location.pk,
        )
        mapping = add_location_mapping(InterventionAbstract.Options.mapping)
