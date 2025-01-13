import datetime

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.paginator import Paginator
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext as _

from celery.utils.log import get_task_logger
from dynamic_serializer.core import get_attr

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.models import T2FTravel, T2FTravelactivity, T2FTravelattachment

from .base import EtoolsDataMartModel

logger = get_task_logger(__name__)


class TravelAttachment(object):
    pass


class TripLoader(EtoolsLoader):
    """
    --
    SET search_path = public,##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count" FROM "t2f_travelactivity" WHERE "t2f_travelactivity"."date" >= '2023-01-01'::date;

    --
    SELECT '##COUNTRY##' AS __schema,
           "t2f_travelactivity"."id",
           "t2f_travelactivity"."travel_type",
           "t2f_travelactivity"."date",
           "t2f_travelactivity"."partner_id",
           "t2f_travelactivity"."partnership_id",
           "t2f_travelactivity"."primary_traveler_id",
           "t2f_travelactivity"."result_id",

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
           "reports_result"."activity_focus_code",
           "reports_result"."activity_focus_name",
           "reports_result"."hidden", "reports_result"."from_date",
           "reports_result"."to_date", "reports_result"."ram",
           "reports_result"."country_programme_id",
           "reports_result"."created",
           "reports_result"."modified",
           "reports_result"."humanitarian_marker_code",
           "reports_result"."humanitarian_marker_name",
           "reports_result"."programme_area_code",
           "reports_result"."programme_area_name"
    FROM "t2f_travelactivity"
         LEFT OUTER JOIN "partners_partnerorganization" ON ("t2f_travelactivity"."partner_id" = "partners_partnerorganization"."id")
         LEFT OUTER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
         LEFT OUTER JOIN "partners_intervention" ON ("t2f_travelactivity"."partnership_id" = "partners_intervention"."id")
         INNER JOIN "auth_user" ON ("t2f_travelactivity"."primary_traveler_id" = "auth_user"."id")
         LEFT OUTER JOIN "reports_result" ON ("t2f_travelactivity"."result_id" = "reports_result"."id")
    WHERE "t2f_travelactivity"."date" >= '2023-01-01'::date
    ORDER BY "t2f_travelactivity"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT ("t2f_travelactivity_travels"."travelactivity_id") AS "_prefetch_related_val_travelactivity_id",
           '##COUNTRY##' AS __schema,
           "t2f_travel"."id",
           "t2f_travel"."created",
           "t2f_travel"."completed_at",
           "t2f_travel"."canceled_at",
           "t2f_travel"."submitted_at",
           "t2f_travel"."rejected_at",
           "t2f_travel"."approved_at",
           "t2f_travel"."rejection_note",
           "t2f_travel"."cancellation_note",
           "t2f_travel"."certification_note",
           "t2f_travel"."report_note",
           "t2f_travel"."misc_expenses",
           "t2f_travel"."status",
           "t2f_travel"."start_date",
           "t2f_travel"."end_date",
           "t2f_travel"."purpose",
           "t2f_travel"."additional_note",
           "t2f_travel"."international_travel",
           "t2f_travel"."ta_required",
           "t2f_travel"."reference_number",
           "t2f_travel"."hidden",
           "t2f_travel"."mode_of_travel",
           "t2f_travel"."estimated_travel_cost",
           "t2f_travel"."is_driver",
           "t2f_travel"."preserved_expenses_local",
           "t2f_travel"."approved_cost_traveler",
           "t2f_travel"."approved_cost_travel_agencies",
           "t2f_travel"."currency_id",
           "t2f_travel"."office_id",
           "t2f_travel"."supervisor_id",
            "t2f_travel"."traveler_id",
           "t2f_travel"."first_submission_date",
           "t2f_travel"."preserved_expenses_usd",
           "t2f_travel"."section_id"
    FROM "t2f_travel" INNER JOIN "t2f_travelactivity_travels" ON ("t2f_travel"."id" = "t2f_travelactivity_travels"."travel_id")
    WHERE "t2f_travelactivity_travels"."travelactivity_id" IN ( ##LIST OF "t2f_travelactivity"."id" in the page ##);


    -- Adapted to make it prefetch
    SELECT "publics_currency"."id",
           "publics_currency"."name",
           "publics_currency"."code",
           "publics_currency"."decimal_places",
           "publics_currency"."deleted_at"
    FROM "publics_currency" WHERE "publics_currency"."id" in (## LIST OF  "t2f_travel"."currency_id" ## );


    --N+1 query
    SELECT 1 AS "a"
    FROM "t2f_travelattachment"
    WHERE ("t2f_travelattachment"."travel_id" = ##t2f_travel"."id"##
    AND UPPER("t2f_travelattachment"."type"::text)
    LIKE UPPER('HACT Programme Monitoring%')) LIMIT 1


    SELECT "auth_user"."id",
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
    WHERE "auth_user"."id" = ##???## LIMIT 21;


    -- Adapted to make it prefetch
    SELECT 'afghanistan' AS __schema,
           "locations_location"."id",
           "locations_location"."name",
           "locations_location"."latitude",
           "locations_location"."longitude",
           "locations_location"."p_code",
           "locations_location"."point",
           "locations_location"."geom",
           "locations_location"."level",
           "locations_location"."lft",
           "locations_location"."parent_id",
           "locations_location"."rght",
           "locations_location"."tree_id",
           "locations_location"."created",
           "locations_location"."modified",
           "locations_location"."is_active",
           "locations_location"."admin_level",
           "locations_location"."admin_level_name"
    FROM "locations_location"
          INNER JOIN "t2f_travelactivity_locations" ON ("locations_location"."id" = "t2f_travelactivity_locations"."location_id")
    WHERE "t2f_travelactivity_locations"."travelactivity_id" IN (##List of "t2f_travelactivity"."id" in the page ##)
    ORDER BY "locations_location"."id" ASC

    -- Adapted to make it prefetch
    SELECT 'afghanistan' AS __schema,
           "reports_office"."id",
           "reports_office"."name"
    FROM  "reports_office"
    WHERE "reports_office"."id" IN (## List of "t2f_travel"."office_id"  in the page ##);

    -- Adapted to make it prefetch
    SELECT 'afghanistan' AS __schema,
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
    FROM "reports_sector"
    WHERE "reports_sector"."id" IN (##List of "reports_result"."sector_id" ##);
    """

    def remove_deleted(self):
        country = self.context["country"]
        # existing = list(self.get_queryset().only('id').values_list('id', flat=True))
        existing = list(T2FTravelactivity.objects.only("id").values_list("id", flat=True))
        to_delete = self.model.objects.filter(schema_name=country.schema_name).exclude(source_activity_id__in=existing)
        self.results.deleted += to_delete.count()
        to_delete.delete()

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.filter_queryset(self.get_queryset())

        paginator = Paginator(qs.all().order_by("id"), batch_size)

        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for t2f_travel_activity in page.object_list:
                for travel in t2f_travel_activity.travels.all():
                    travel.activity = t2f_travel_activity
                    filters = self.config.key(self, travel)
                    values = self.get_values(travel)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)

    def get_is_second_traveler(self, record: T2FTravel, values: dict, **kwargs):
        return record.traveler != record.activity.primary_traveler

    def get_attachments(self, record: T2FTravel, values: dict, **kwargs):
        return ",\n".join(list(map(lambda x: ":".join(x), record.attachments.values_list("type", "file"))))

    def get_hact_visit_report(self, record: T2FTravel, values: dict, **kwargs):
        return (
            "Yes"
            if T2FTravelattachment.objects.filter(
                travel=record,
                type__istartswith="HACT Programme Monitoring",
            ).exists()
            else ""
        )

    def get_locations(self, record: T2FTravel, values: dict, **kwargs):
        # PartnersInterventionFlatLocations
        locs = []
        # intervention: PartnersIntervention = original.activity.intervention
        for location in record.activity.locations.order_by("id"):
            locs.append(
                dict(
                    source_id=location.id,
                    name=location.name,
                    pcode=location.p_code,
                    level=location.level,
                    levelname=location.admin_level_name,
                )
            )
        values["locations_data"] = locs
        return ", ".join([loc["name"] for loc in locs])

    def get_trip_attachments(self, record, values, **kwargs):
        return ",\n".join(
            list(map(lambda x: ":".join(x), record.T2FTravelattachment_travel.values_list("type", "file")))
        )


class ModeOfTravel:
    PLANE = "Plane"
    BUS = "Bus"
    CAR = "Car"
    BOAT = "Boat"
    RAIL = "Rail"
    CHOICES = ((PLANE, "Plane"), (BUS, "Bus"), (CAR, "Car"), (BOAT, "Boat"), (RAIL, "Rail"))


class Trip(EtoolsDataMartModel):
    PLANNED = "planned"
    SUBMITTED = "submitted"
    REJECTED = "rejected"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

    CHOICES = (
        (PLANNED, _("Planned")),
        (SUBMITTED, _("Submitted")),
        (REJECTED, _("Rejected")),
        (APPROVED, _("Approved")),
        (COMPLETED, _("Completed")),
        (CANCELLED, _("Cancelled")),
        (COMPLETED, _("Completed")),
    )
    additional_note = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    cancellation_note = models.TextField(blank=True, null=True)
    certification_note = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cp_output = models.TextField(blank=True, null=True)
    cp_output_id = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)
    estimated_travel_cost = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    hact_visit_report = models.CharField(max_length=300, blank=True, null=True)
    hidden = models.BooleanField(blank=True, null=True)
    international_travel = models.BooleanField(blank=True, null=True)
    is_driver = models.BooleanField(blank=True, null=True)
    is_second_traveler = models.CharField(max_length=300, blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True)
    misc_expenses = models.TextField(blank=True, null=True)
    mode_of_travel = ArrayField(
        models.CharField(max_length=5, choices=ModeOfTravel.CHOICES),
        null=True,
        blank=True,
        db_index=True,
        default=list,
        verbose_name=_("Mode of Travel"),
    )

    office_name = models.CharField(max_length=300, blank=True, null=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    pd_ssfa_reference_number = models.CharField(max_length=300, blank=True, null=True)
    pd_ssfa_title = models.CharField(max_length=300, blank=True, null=True)
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    primary_traveler = models.CharField(max_length=300, blank=True, null=True)
    purpose = models.CharField(max_length=500, blank=True, null=True)
    reference_number = models.CharField(max_length=12, blank=True, null=True, db_index=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejection_note = models.TextField(blank=True, null=True)
    report_note = models.TextField(blank=True, null=True)
    section_name = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=50, choices=CHOICES, blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    supervisor_email = models.CharField(max_length=300, blank=True, null=True)
    supervisor_name = models.CharField(max_length=300, blank=True, null=True)
    ta_required = models.BooleanField(blank=True, null=True)
    traveler_email = models.CharField(max_length=300, blank=True, null=True)
    traveler_name = models.CharField(max_length=300, blank=True, null=True)
    trip_attachments = models.TextField(blank=True, null=True)
    trip_activity_date = models.DateField(blank=True, null=True)
    trip_activity_type = models.CharField(max_length=300, blank=True, null=True)
    trip_activity_reference_number = models.CharField(max_length=300, blank=True, null=True)
    trip_url = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=300, blank=True, null=True)

    source_activity_id = models.IntegerField(blank=True, null=True)
    loader = TripLoader()

    class Meta:
        unique_together = ("schema_name", "source_id", "source_activity_id")

    class Options:
        source = T2FTravelactivity
        ordering_fields = ("id",)
        ordering = "id"
        # last_modify_field = 'modified'
        sync_deleted_records = lambda a: False
        key = lambda loader, travel: dict(
            schema_name=loader.context["country"].schema_name,
            source_id=travel.id,
            source_activity_id=travel.activity.id,
        )
        queryset = (
            lambda: T2FTravelactivity.objects.filter(date__year__gte=datetime.datetime.now().year - settings.YEAR_DELTA)
            .select_related(
                "result",
                "partner",
                "partner__organization",
                "partnership",
                "primary_traveler",
            )
            .prefetch_related("travels")
            # TODO:  Prefetch improvements on travels, t2f_travelattachment, auth_user
        )
        mapping = dict(
            # cp_output="activity.result.name",
            cp_output="i",
            cp_output_id="activity.result.vision_id",
            currency_code="currency.code",
            is_second_traveler="-",
            locations="-",
            locations_data="i",
            office_name="office.name",
            partner_name="activity.partner.organization.name",
            pd_ssfa_reference_number="activity.partnership.number",
            pd_ssfa_title="activity.partnership.title",
            primary_traveler="activity.primary_traveler.email",
            section_name="section.name",
            supervisor_email="supervisor.email",
            supervisor_name=lambda loader, record: "%s %s"
            % (get_attr(record, "supervisor.last_name"), get_attr(record, "supervisor.first_name")),
            traveler_email="traveler.email",
            traveler_name=lambda loader, record: "%s %s" % (record.traveler.last_name, record.traveler.first_name),
            trip_attachments="-",
            trip_activity_date="activity.date",
            trip_activity_reference_number="activity.reference_number",
            trip_activity_type="activity.travel_type",
            trip_url=lambda loader, record: "t2f/edit-travel/%s" % record.id,
            vendor_number="activity.partner.organization.vendor_number",
            source_activity_id="activity.id",
        )
