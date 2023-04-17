from datetime import date, datetime, timezone

from django.db import models
from django.db.models import Exists, F, JSONField, Max, OuterRef

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import (
    AuditEngagementConsts,
    FieldMonitoringPlanningMonitoringactivityConst,
    PartnerOrganizationConst,
    PartnerType,
    T2FTravelConsts,
    TpmTpmvisitConst,
    TravelType,
)
from etools_datamart.apps.sources.etools.models import (
    AuditSpotcheck,
    FieldMonitoringDataCollectionActivityquestionoverallfinding,
    FieldMonitoringPlanningMonitoringactivity,
    FieldMonitoringPlanningMonitoringactivitygroup,
    PartnersPartnerorganization,
    T2FTravel,
    TpmTpmactivity,
    TpmTpmvisit,
)


class PartnerHactLoader(EtoolsLoader):
    def get_queryset(self):
        return PartnersPartnerorganization.objects.prefetch_related(
            "ActivitiesActivity_partner__TpmTpmactivity_activity_ptr",
            "FieldMonitoringPlanningMonitoringactivitygroup_partner",
        )

    def get_programmatic_visits(self, record, values, **kwargs):
        pv_year = T2FTravel.objects.filter(
            t2ftravelactivity__travel_type=TravelType.PROGRAMME_MONITORING,
            traveler=F("t2ftravelactivity__primary_traveler"),
            status=T2FTravelConsts.COMPLETED,
            end_date__year=datetime.now().year,
            t2ftravelactivity__partner=record,
        )
        tpmv = record.ActivitiesActivity_partner.filter(
            TpmTpmactivity_activity_ptr__is_pv=True,
            TpmTpmactivity_activity_ptr__tpm_visit__status=TpmTpmvisitConst.UNICEF_APPROVED,
            date__year=datetime.now().year,
        )

        # fmvgs = (
        #     FieldMonitoringPlanningMonitoringactivitygroup.objects.filter(
        #         partner=record,
        #         FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc_monitoringactivitygroup__monitoringactivity__status="completed",
        #     )
        #     .annotate(
        #         end_date=Max(
        #             "FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc_monitoringactivitygroup__monitoringactivity__end_date"
        #         ),
        #     )
        #     .filter(end_date__year=datetime.now().year)
        #     .distinct()
        # )

        # field monitoring activities qualify as programmatic visits if during a monitoring activity the hact
        # question was answered with an overall rating and the visit is completed
        grouped_activities = record.FieldMonitoringPlanningMonitoringactivitygroup_partner.values_list(
            "FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc_monitoringactivitygroup__monitoringactivity__id",
            flat=True,
        )

        question_sq = FieldMonitoringDataCollectionActivityquestionoverallfinding.objects.filter(
            activity_question__monitoring_activity_id=OuterRef("id"),
            activity_question__question__is_hact=True,
            activity_question__question__level="partner",
            value__isnull=False,
        )

        fmvqs = (
            FieldMonitoringPlanningMonitoringactivity.objects.filter(
                end_date__year=datetime.now().year,
            )
            .annotate(is_hact=Exists(question_sq))
            .filter(
                FieldMonitoringPlanningMonitoringactivityPartners_monitoringactivity__partnerorganization=record.id,
                status=FieldMonitoringPlanningMonitoringactivityConst.STATUS_COMPLETED,
                is_hact=True,
            )
            .exclude(
                id__in=grouped_activities,
            )
        )

        visits = []
        t2f_visits = pv_year or []
        for visit in t2f_visits:
            visits.append(
                {"module": "t2f", "end_date": str(visit.end_date), "reference_number": visit.reference_number}
            )

        tpm_visits = tpmv
        for visit in tpm_visits:
            visits.append(
                {
                    "module": "tpm",
                    "end_date": str(visit.activity_ptr.date),
                    "reference_number": visit.tpm_visit.reference_number,
                }
            )

        # fm_visits = fmvgs
        # for visit in fm_visits:
        #     visits.append({
        #         'module': 'fm',
        #         'date': str(max([monitor_activity.end_date for monitor_activity in visit.monitoring_activities.all()])),
        #         'reference_number': ', '.join([
        #             monitor_activity.number for monitor_activity in visit.monitoring_activities.all()
        #         ])
        #     })
        fm_visits = fmvqs
        for monitor_activity in fm_visits:
            visits.append(
                {"module": "fm", "date": str(monitor_activity.end_date), "reference_number": monitor_activity.number}
            )

        return visits

    def get_spot_checks(self, record, values, **kwargs):
        def reference_number(spot_check):
            if spot_check.engagement_ptr.engagement_type == AuditEngagementConsts.TYPE_AUDIT:
                engagement_code = "a"
            else:
                engagement_code = spot_check.engagement_ptr.engagement_type
            return "{}/{}/{}/{}/{}".format(
                spot_check.schema or "",
                spot_check.engagement_ptr.partner.name[:5],
                engagement_code.upper(),
                spot_check.engagement_ptr.created.year,
                spot_check.engagement_ptr.id,
            )

        spot_checks = AuditSpotcheck.objects.filter(
            engagement_ptr__partner=record, engagement_ptr__date_of_draft_report_to_ip__year=datetime.now().year
        ).exclude(engagement_ptr__status=AuditEngagementConsts.CANCELLED)

        scs = []
        for spot_check in spot_checks:
            scs.append(
                {
                    "date": str(spot_check.engagement_ptr.date_of_draft_report_to_ip),
                    "reference_number": reference_number(spot_check),
                }
            )
        return scs


class PartnerHact(EtoolsDataMartModel):
    # EXPIRING_ASSESSMENT_LIMIT_YEAR = 4
    # CT_CP_AUDIT_TRIGGER_LEVEL = decimal.Decimal('50000.00')
    # RATING_NOT_REQUIRED = 'Not Required'

    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    vendor_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_index=True,
    )
    short_name = models.CharField(max_length=50, blank=True, null=True)
    type_of_assessment = models.CharField(max_length=50, blank=True, null=True)
    partner_type = models.CharField(max_length=50, db_index=True, blank=True, null=True, choices=PartnerType.CHOICES)
    cso_type = models.CharField(
        max_length=50, blank=True, null=True, db_index=True, choices=PartnerOrganizationConst.CSO_TYPES
    )
    rating = models.CharField(
        max_length=50, blank=True, null=True, db_index=True, choices=PartnerOrganizationConst.RISK_RATINGS
    )
    hact_values = JSONField(blank=True, null=True)  # This field type is a guess.
    hact_min_requirements = JSONField(default=dict, blank=True, null=True)

    programmatic_visits = JSONField(default=dict, blank=True, null=True)
    spot_checks = JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ("name",)
        unique_together = (
            ("schema_name", "name", "vendor_number"),
            ("schema_name", "vendor_number"),
        )

    loader = PartnerHactLoader()

    class Options:
        source = PartnersPartnerorganization
        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name,
            source_id=record.id,
        )
