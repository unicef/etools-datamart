import decimal
from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, JSONField, Prefetch
from django.utils.translation import gettext_lazy as _

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import PartnerOrganizationConst, PartnerType, TravelType
from etools_datamart.apps.sources.etools.models import PartnersPartnerorganization, ReportsOffice, T2FTravelactivity


class PartnerLoader(EtoolsLoader):
    """
    -- To run per country schema
    SET search_path = public,##COUNTRY##;

    -- Count for paging
    SELECT COUNT(*) AS "__count" FROM "partners_partnerorganization;

    -- Partner Organization
    SELECT '##COUNTRY##' AS __schema,
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

           "reports_office"."id",
           "reports_office"."name", '

           "reports_sector"."id",
           "reports_sector"."name",
           "reports_sector"."description",
           "reports_sector"."alternate_id",
           "reports_sector"."alternate_name",
           "reports_sector"."dashboard",
           "reports_sector"."color",
           "reports_sector"."created",
           "reports_sector"."modified",
           "reports_sector"."active",

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

           "partners_plannedengagement"."id",
           "partners_plannedengagement"."created",
           "partners_plannedengagement"."modified",
           "partners_plannedengagement"."spot_check_planned_q1",
           "partners_plannedengagement"."spot_check_planned_q2",
           "partners_plannedengagement"."spot_check_planned_q3",
           "partners_plannedengagement"."spot_check_planned_q4",
           "partners_plannedengagement"."scheduled_audit",
           "partners_plannedengagement"."special_audit",
           "partners_plannedengagement"."spot_check_follow_up",
           "partners_plannedengagement"."partner_id"
    FROM "partners_partnerorganization"
    LEFT OUTER JOIN "reports_office" ON ("partners_partnerorganization"."lead_office_id" = "reports_office"."id")
    LEFT OUTER JOIN "reports_sector" ON ("partners_partnerorganization"."lead_section_id" = "reports_sector"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    LEFT OUTER JOIN "partners_plannedengagement" ON ("partners_partnerorganization"."id" = "partners_plannedengagement"."partner_id")
    ORDER BY "partners_partnerorganization"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;


    --  Travel Activity
    SELECT  '##COUNTRY##' AS __schema,
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
    WHERE ("t2f_travelactivity"."date" IS NOT NULL AND "t2f_travelactivity"."travel_type" = 'Programmatic Visit'
           AND "t2f_travel"."status" = 'completed' AND "t2f_travel"."traveler_id" = ("t2f_travelactivity"."primary_traveler_id")
           AND "t2f_travelactivity"."partner_id" IN (##PARTNER_ID_LIST_IN_THE_PAGE##)
    ORDER BY "t2f_travelactivity"."date" DESC;

    """

    def get_queryset(self):
        return (
            PartnersPartnerorganization.objects.select_related(
                "planned_engagement",
                "organization",
                "lead_office",
                "lead_section",
            )
            .prefetch_related(
                Prefetch(
                    "T2FTravelactivity_partner",
                    queryset=T2FTravelactivity.objects.filter(
                        travel_type=TravelType.PROGRAMME_MONITORING,
                        date__isnull=False,
                        travels__status="completed",
                        travels__traveler=F("primary_traveler"),
                    ).order_by("-date"),
                ),
            )
            .all()
            # TODO:Try getting only the required fields
        )

    def get_last_pv_date(self, record, values, **kwargs):
        activity_date = None
        for activity in record.T2FTravelactivity_partner.all():
            return activity.date
        return activity_date

    def get_planned_engagement(self, record, values, **kwargs):
        try:
            rec = record.planned_engagement
            data = {
                "spot_check_planned_q1": rec.spot_check_planned_q1,
                "spot_check_planned_q2": rec.spot_check_planned_q2,
                "spot_check_planned_q3": rec.spot_check_planned_q3,
                "spot_check_planned_q4": rec.spot_check_planned_q4,
                "scheduled_audit": rec.scheduled_audit,
                "special_audit": rec.special_audit,
                "required_audit": sum([rec.special_audit, rec.scheduled_audit]),
                "spot_check_follow_up": rec.spot_check_follow_up,
            }
        except BaseException:
            data = {}
        return data

    def get_lead_office(self, record, values, **kwargs):
        office = getattr(record, "lead_office", None)
        return office.name if office else None

    def get_lead_section(self, record, values, **kwargs):
        section = getattr(record, "lead_section", None)
        return section.name if section else None

    def get_expiring_assessment_flag(self, record, **kwargs):
        if record.last_assessment_date:
            last_assessment_age = date.today().year - record.last_assessment_date.year
            return last_assessment_age >= Partner.EXPIRING_ASSESSMENT_LIMIT_YEAR
        return False

    def get_expiring_psea_assessment_flag(self, record, **kwargs):
        if record.psea_assessment_date:
            last_assessment_age = date.today().year - record.psea_assessment_date.year
            return last_assessment_age >= Partner.EXPIRING_ASSESSMENT_LIMIT_YEAR
        return False

    def get_approaching_threshold_flag(self, record, **kwargs):
        total_ct_ytd = record.total_ct_ytd or 0
        not_required = record.highest_risk_rating_name == Partner.RATING_NOT_REQUIRED
        ct_year_overflow = total_ct_ytd > Partner.CT_CP_AUDIT_TRIGGER_LEVEL
        return not_required and ct_year_overflow


class Partner(EtoolsDataMartModel):
    EXPIRING_ASSESSMENT_LIMIT_YEAR = 4
    CT_CP_AUDIT_TRIGGER_LEVEL = decimal.Decimal("50000.00")
    RATING_NOT_REQUIRED = "Not Required"

    address = models.TextField(blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    basis_for_risk_rating = models.CharField(max_length=50, blank=True, null=True)
    blocked = models.BooleanField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    core_values_assessment_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    cso_type = models.CharField(
        max_length=50, blank=True, null=True, db_index=True, choices=PartnerOrganizationConst.CSO_TYPES
    )
    deleted_flag = models.BooleanField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    hact_values = JSONField(blank=True, null=True)  # This field type is a guess.
    hidden = models.BooleanField(db_index=True, blank=True, null=True)
    last_assessment_date = models.DateField(blank=True, null=True)
    manually_blocked = models.BooleanField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    net_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    outstanding_dct_amount_6_to_9_months_usd = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    outstanding_dct_amount_more_than_9_months_usd = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    partner_type = models.CharField(max_length=50, db_index=True, blank=True, null=True, choices=PartnerType.CHOICES)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    postal_code = models.CharField(max_length=32, blank=True, null=True)
    rating = models.CharField(
        max_length=50, blank=True, null=True, db_index=True, choices=PartnerOrganizationConst.RISK_RATINGS
    )
    reported_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    shared_with = ArrayField(
        models.CharField(max_length=20, blank=True, choices=PartnerOrganizationConst.AGENCY_CHOICES),
        verbose_name=_("Shared Partner"),
        blank=True,
        null=True,
        default=list,
    )
    short_name = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=500, blank=True, null=True)
    total_ct_cp = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_ytd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    type_of_assessment = models.CharField(max_length=50, blank=True, null=True)
    vendor_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_index=True,
    )
    vision_synced = models.BooleanField(blank=True, null=True)

    # Model property
    min_req_programme_visits = models.IntegerField(default=0, blank=True, null=True)
    hact_min_requirements = JSONField(default=dict, blank=True, null=True)
    min_req_spot_checks = models.IntegerField(default=0, blank=True, null=True)

    # O2O
    planned_engagement = JSONField(default=dict, blank=True, null=True)

    last_pv_date = models.DateField(blank=True, null=True, db_index=True)
    sea_risk_rating_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    highest_risk_rating_name = models.CharField(max_length=150, blank=True, null=True)
    highest_risk_rating_type = models.CharField(max_length=150, blank=True, null=True)
    psea_assessment_date = models.DateTimeField(null=True, blank=True)
    lead_office = models.CharField(max_length=254, null=True, blank=True)
    lead_section = models.CharField(max_length=128, null=True, blank=True)

    expiring_assessment_flag = models.BooleanField(blank=True, null=True)
    expiring_psea_assessment_flag = models.BooleanField(blank=True, null=True)
    approaching_threshold_flag = models.BooleanField(blank=True, null=True)

    class Meta:
        ordering = ("name",)
        unique_together = (
            ("schema_name", "name", "vendor_number"),
            ("schema_name", "vendor_number"),
        )

    loader = PartnerLoader()

    class Options:
        source = PartnersPartnerorganization
        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name,
            source_id=record.id,
        )
        mapping = dict(
            name="organization.name",
            vendor_number="organization.vendor_number",
            partner_type="organization.organization_type",
            cso_type="organization.cso_type",
            short_name="organization.short_name",
        )
