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
    """

    -- For each country;
    --
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "partners_partnerorganization";

    --
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

          "organizations_organization"."id",
          "organizations_organization"."created",
          "organizations_organization"."modified",
          "organizations_organization"."name",
          "organizations_organization"."vendor_number",
          "organizations_organization"."organization_type",
          "organizations_organization"."cso_type",
          "organizations_organization"."short_name",
          "organizations_organization"."other",
          "organizations_organization"."parent_id"
    FROM "partners_partnerorganization"
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    ORDER BY "partners_partnerorganization"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT '##COUNTRY##' AS __schema,
           "activities_activity"."id",
           "activities_activity"."date",
           "activities_activity"."cp_output_id",
           "activities_activity"."intervention_id",
           "activities_activity"."partner_id"
    FROM "activities_activity"
    WHERE "activities_activity"."partner_id" IN (## LIST OF ##);

    --
    SELECT ''##COUNTRY##' AS __schema,
            "tpm_tpmactivity"."activity_ptr_id",
            "tpm_tpmactivity"."additional_information",
            "tpm_tpmactivity"."is_pv",
            "tpm_tpmactivity"."tpm_visit_id",
            "tpm_tpmactivity"."section_id"
    FROM "tpm_tpmactivity"
    WHERE "tpm_tpmactivity"."activity_ptr_id" IN (##LIST OF "activities_activity"."id" for the PAGE##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_planning_monitoringactivitygroup"."id",
           "field_monitoring_planning_monitoringactivitygroup"."partner_id"
    FROM "field_monitoring_planning_monitoringactivitygroup"
    WHERE "field_monitoring_planning_monitoringactivitygroup"."partner_id" IN (##  ##);

    --
    SELECT '##COUNTRY##' AS __schema,
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
    FROM "t2f_travel"
    INNER JOIN "t2f_travelactivity_travels" ON ("t2f_travel"."id" = "t2f_travelactivity_travels"."travel_id")
    INNER JOIN "t2f_travelactivity" ON ("t2f_travelactivity_travels"."travelactivity_id" = "t2f_travelactivity"."id")
    WHERE ("t2f_travel"."end_date" BETWEEN '2024-01-01'::date AND '2024-12-31'::date AND "t2f_travel"."status" = 'completed'
    AND "t2f_travelactivity"."partner_id" IN (##  ##)
    AND "t2f_travelactivity"."travel_type" = 'Programmatic Visit'
    AND "t2f_travel"."traveler_id" = ("t2f_travelactivity"."primary_traveler_id"));

    --
    SELECT '##COUNTRY##' AS __schema,
           "tpm_tpmactivity"."activity_ptr_id",
           "tpm_tpmactivity"."additional_information",
           "tpm_tpmactivity"."is_pv",
           "tpm_tpmactivity"."tpm_visit_id",
           "tpm_tpmactivity"."section_id"
    FROM "tpm_tpmactivity"
    INNER JOIN "activities_activity" ON ("tpm_tpmactivity"."activity_ptr_id" = "activities_activity"."id")
    INNER JOIN "tpm_tpmvisit" ON ("tpm_tpmactivity"."tpm_visit_id" = "tpm_tpmvisit"."id")
    WHERE ("activities_activity"."date" BETWEEN '2024-01-01'::date AND '2024-12-31'::date AND "activities_activity"."partner_id" = 1 AND "tpm_tpmactivity"."is_pv" AND "tpm_tpmvisit"."status" = 'unicef_approved')

    --
    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_planning_monitoringactivity"."id",
           "field_monitoring_planning_monitoringactivity"."created",
           "field_monitoring_planning_monitoringactivity"."modified",
           "field_monitoring_planning_monitoringactivity"."deleted_at",
           "field_monitoring_planning_monitoringactivity"."monitor_type",
           "field_monitoring_planning_monitoringactivity"."start_date",
           "field_monitoring_planning_monitoringactivity"."end_date",
           "field_monitoring_planning_monitoringactivity"."status",
           "field_monitoring_planning_monitoringactivity"."location_id",
           "field_monitoring_planning_monitoringactivity"."location_site_id",
           "field_monitoring_planning_monitoringactivity"."visit_lead_id",
           "field_monitoring_planning_monitoringactivity"."tpm_partner_id",
           "field_monitoring_planning_monitoringactivity"."cancel_reason",
           "field_monitoring_planning_monitoringactivity"."reject_reason",
           "field_monitoring_planning_monitoringactivity"."field_office_id",
           "field_monitoring_planning_monitoringactivity"."report_reject_reason",
           "field_monitoring_planning_monitoringactivity"."number",
            EXISTS(SELECT 1 AS "a" FROM "field_monitoring_data_collection_activityquestionoverallfinding" U0 INNER JOIN "field_monitoring_data_collection_activityquestion" U1 ON (U0."activity_question_id" = U1."id")
                   INNER JOIN "field_monitoring_settings_question" U3 ON (U1."question_id" = U3."id")
                   WHERE (U1."monitoring_activity_id" = ("field_monitoring_planning_monitoringactivity"."id") AND U3."is_hact" AND U3."level" = 'partner' AND U0."value" IS NOT NULL) LIMIT 1) AS "is_hact"
             FROM "field_monitoring_planning_monitoringactivity"
             INNER JOIN "field_monitoring_planning_monitoringactivity_partners" ON ("field_monitoring_planning_monitoringactivity"."id" = "field_monitoring_planning_monitoringactivity_partners"."monitoringactivity_id")
             WHERE ("field_monitoring_planning_monitoringactivity"."end_date" BETWEEN '2024-01-01'::date AND '2024-12-31'::date AND "field_monitoring_planning_monitoringactivity_partners"."partnerorganization_id" = 1
             AND EXISTS(SELECT 1 AS "a" FROM "field_monitoring_data_collection_activityquestionoverallfinding" U0 INNER JOIN "field_monitoring_data_collection_activityquestion" U1 ON (U0."activity_question_id" = U1."id")
             INNER JOIN "field_monitoring_settings_question" U3 ON (U1."question_id" = U3."id") WHERE (U1."monitoring_activity_id" = ("field_monitoring_planning_monitoringactivity"."id") AND U3."is_hact"
             AND U3."level" = 'partner' AND U0."value" IS NOT NULL) LIMIT 1) AND "field_monitoring_planning_monitoringactivity"."status" = 'completed' AND NOT ("field_monitoring_planning_monitoringactivity"."id" IN (SELECT U2."monitoringactivity_id"
    FROM "field_monitoring_planning_monitoringactivitygroup" U0 LEFT OUTER JOIN "field_monitoring_planning_monitoringactivitygroup_monitorin69fc" U2 ON (U0."id" = U2."monitoringactivitygroup_id") WHERE U0."partner_id" = 1)))

    --
    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_planning_monitoringactivity"."id",
           "field_monitoring_planning_monitoringactivity"."created",
           "field_monitoring_planning_monitoringactivity"."modified",
           "field_monitoring_planning_monitoringactivity"."deleted_at",
           "field_monitoring_planning_monitoringactivity"."monitor_type",
           "field_monitoring_planning_monitoringactivity"."start_date",
           "field_monitoring_planning_monitoringactivity"."end_date",
           "field_monitoring_planning_monitoringactivity"."status",
           "field_monitoring_planning_monitoringactivity"."location_id",
           "field_monitoring_planning_monitoringactivity"."location_site_id",
           "field_monitoring_planning_monitoringactivity"."visit_lead_id",
           "field_monitoring_planning_monitoringactivity"."tpm_partner_id",
           "field_monitoring_planning_monitoringactivity"."cancel_reason",
           "field_monitoring_planning_monitoringactivity"."reject_reason",
           "field_monitoring_planning_monitoringactivity"."field_office_id",
           "field_monitoring_planning_monitoringactivity"."report_reject_reason",
           "field_monitoring_planning_monitoringactivity"."number",
            EXISTS(SELECT 1 AS "a" FROM
                   "field_monitoring_data_collection_activityquestionoverallfinding" U0
                    INNER JOIN "field_monitoring_data_collection_activityquestion" U1 ON (U0."activity_question_id" = U1."id")
                    INNER JOIN "field_monitoring_settings_question" U3 ON (U1."question_id" = U3."id")
                    WHERE (U1."monitoring_activity_id" = ("field_monitoring_planning_monitoringactivity"."id")
                    AND U3."is_hact" AND U3."level" = 'partner' AND U0."value" IS NOT NULL) LIMIT 1) AS "is_hact"
           FROM "field_monitoring_planning_monitoringactivity"
           INNER JOIN "field_monitoring_planning_monitoringactivity_partners" ON ("field_monitoring_planning_monitoringactivity"."id" = "field_monitoring_planning_monitoringactivity_partners"."monitoringactivity_id")
           WHERE ("field_monitoring_planning_monitoringactivity"."end_date" BETWEEN '2024-01-01'::date AND '2024-12-31'::date
                  AND "field_monitoring_planning_monitoringactivity_partners"."partnerorganization_id" = 476
                  AND EXISTS(
                    SELECT 1 AS "a" FROM "field_monitoring_data_collection_activityquestionoverallfinding" U0 INNER JOIN "field_monitoring_data_collection_activityquestion" U1 ON (U0."activity_question_id" = U1."id")
                    INNER JOIN "field_monitoring_settings_question" U3 ON (U1."question_id" = U3."id")
                    WHERE (U1."monitoring_activity_id" = ("field_monitoring_planning_monitoringactivity"."id")
                    AND U3."is_hact" AND U3."level" = 'partner' AND U0."value" IS NOT NULL) LIMIT 1)
                    AND "field_monitoring_planning_monitoringactivity"."status" = 'completed'
                    AND NOT ("field_monitoring_planning_monitoringactivity"."id"
                    IN (SELECT U2."monitoringactivity_id"
                          FROM "field_monitoring_planning_monitoringactivitygroup" U0 LEFT OUTER JOIN "field_monitoring_planning_monitoringactivitygroup_monitorin69fc" U2 ON (U0."id" = U2."monitoringactivitygroup_id")
                        WHERE U0."partner_id" = 476)))

    --
    SELECT '##COUNTRY##' AS __schema,
           "audit_spotcheck"."engagement_ptr_id",
           "audit_spotcheck"."total_amount_tested",
           "audit_spotcheck"."total_amount_of_ineligible_expenditure",
           "audit_spotcheck"."internal_controls"
           FROM "audit_spotcheck"
           INNER JOIN "audit_engagement" ON ("audit_spotcheck"."engagement_ptr_id" = "audit_engagement"."id")
           WHERE ("audit_engagement"."date_of_draft_report_to_ip" BETWEEN '2024-01-01'::date AND '2024-12-31'::date
                 AND "audit_engagement"."partner_id" = 476 AND NOT ("audit_engagement"."status" = 'cancelled'))

    """

    # TODO: Add Prefetch
    def get_queryset(self):
        return PartnersPartnerorganization.objects.select_related(
            "organization",
        ).prefetch_related(
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
        tpmv = TpmTpmactivity.objects.filter(
            is_pv=True,
            activity_ptr__partner=record,
            tpm_visit__status=TpmTpmvisitConst.UNICEF_APPROVED,
            activity_ptr__date__year=datetime.now().year,
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
        # TODO: use actually prefetched records.
        grouped_activities = record.FieldMonitoringPlanningMonitoringactivitygroup_partner.values_list(
            "FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc_monitoringactivitygroup__monitoringactivity__id",
            flat=True,
        )

        # TODO: Try to load this as a prefetched data
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
                spot_check.engagement_ptr.partner.organization.name[:5],
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
        mapping = dict(
            name="organization.name",
            vendor_number="organization.vendor_number",
            partner_type="organization.organization_type",
            cso_type="organization.cso_type",
            short_name="organization.short_name",
        )
