import decimal
from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, JSONField
from django.utils.translation import gettext_lazy as _

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import PartnerOrganizationConst, PartnerType, TravelType
from etools_datamart.apps.sources.etools.models import PartnersPartnerorganization, T2FTravelactivity


class PartnerLoader(EtoolsLoader):
    def get_queryset(self):
        return PartnersPartnerorganization.objects.select_related("planned_engagement", "organization").all()

    def get_last_pv_date(self, record, values, **kwargs):
        # FIXME: improves this
        activity = T2FTravelactivity.objects.filter(
            partnership__agreement__partner=record,
            travel_type=TravelType.PROGRAMME_MONITORING,
            date__isnull=False,
            travels__status="completed",
            travels__traveler=F("primary_traveler"),
        ).first()
        if activity:
            return activity.date

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
                "required_audit": sum(rec.special_audit, rec.scheduled_audit),
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
