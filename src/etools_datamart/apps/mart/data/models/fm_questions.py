import datetime

from django.conf import settings
from django.db import models, transaction
from django.db.models import F, JSONField, OuterRef, Prefetch, Q, Subquery
from django.utils.translation import gettext as _

import pandas as pd
from celery.utils.log import get_task_logger

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import (
    FieldMonitoringDataCollectionActivityoverallfinding,
    FieldMonitoringDataCollectionActivityquestionoverallfinding,
    FieldMonitoringDataCollectionChecklistoverallfinding,
    FieldMonitoringDataCollectionFinding,
    FieldMonitoringSettingsMethod,
    FieldMonitoringSettingsOption,
    FieldMonitoringSettingsQuestionMethods,
    ReportsSector,
)

logger = get_task_logger(__name__)


def extract_latitude(location):
    if location.latitude is not None:
        return location.latitude
    elif location.point is not None:
        return location.point.y
    elif location.geom is not None:
        return location.centroid.y
    else:
        return None


def extract_longitude(location):
    if location.longitude is not None:
        return location.longitude
    elif location.point is not None:
        return location.point.x
    elif location.geom is not None:
        return location.centroid.x
    else:
        return None


class FMQuestionLoader(EtoolsLoader):
    """
    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_data_collection_finding"."id",
           "field_monitoring_data_collection_finding"."value",
           "field_monitoring_data_collection_finding"."activity_question_id",
           "field_monitoring_data_collection_finding"."started_checklist_id",
           "field_monitoring_settings_locationsite"."name" AS "site_name",
           "locations_location"."name" AS "location_name",

           (SELECT U0."narrative_finding"
            FROM "field_monitoring_data_collection_checklistoverallfinding" U0
            WHERE (U0."started_checklist_id" = ("field_monitoring_data_collection_finding"."started_checklist_id")
            AND (U0."partner_id" = ("field_monitoring_data_collection_activityquestion"."partner_id")
                 OR U0."cp_output_id" = ("field_monitoring_data_collection_activityquestion"."cp_output_id")
                 OR U0."intervention_id" = ("field_monitoring_data_collection_activityquestion"."intervention_id"))) LIMIT 1) AS "narrative_overall_finding",

            "field_monitoring_data_collection_finding"."value" AS "myvalue",

            "field_monitoring_data_collection_activityquestion"."specific_details",
            "field_monitoring_data_collection_activityquestion"."is_enabled",
            "field_monitoring_data_collection_activityquestion"."cp_output_id",
            "field_monitoring_data_collection_activityquestion"."intervention_id",
            "field_monitoring_data_collection_activityquestion"."monitoring_activity_id",
            "field_monitoring_data_collection_activityquestion"."partner_id",
            "field_monitoring_data_collection_activityquestion"."question_id",
            "field_monitoring_data_collection_activityquestion"."is_hact",
            "field_monitoring_data_collection_activityquestion"."text",

            "reports_result"."name", "reports_result"."code",
            "reports_result"."result_type_id",
            "reports_result"."sector_id",
            "reports_result"."gic_code",
            "reports_result"."gic_name",
            "reports_result"."humanitarian_tag",
            "reports_result"."level", "reports_result"."lft",
            "reports_result"."parent_id",
            "reports_result"."rght",
            "reports_result"."sic_code",
            "reports_result"."sic_name",
            "reports_result"."tree_id",
            "reports_result"."vision_id",
            "reports_result"."wbs",
            "reports_result"."activity_focus_code",
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
            "reports_result"."programme_area_name",

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
            "partners_intervention"."final_review_approved", "partners_intervention"."other_details",
            "partners_intervention"."partner_authorized_officer_signatory_id",


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
            "field_monitoring_planning_monitoringactivity"."number", 'botswana' AS __schema,

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
            "locations_location"."admin_level_name",

            "field_monitoring_settings_locationsite"."id", "
            "field_monitoring_settings_locationsite"."created",
            "field_monitoring_settings_locationsite"."modified",
            "field_monitoring_settings_locationsite"."name",
            "field_monitoring_settings_locationsite"."p_code",
            "field_monitoring_settings_locationsite"."point",
            "field_monitoring_settings_locationsite"."is_active",
            "field_monitoring_settings_locationsite"."parent_id",

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

            "field_monitoring_settings_question"."id",
            "field_monitoring_settings_question"."answer_type",
            "field_monitoring_settings_question"."choices_size",
            "field_monitoring_settings_question"."level",
            "field_monitoring_settings_question"."text",
            "field_monitoring_settings_question"."is_hact",
            "field_monitoring_settings_question"."is_custom",
            "field_monitoring_settings_question"."is_active",
            "field_monitoring_settings_question"."category_id",

            "field_monitoring_settings_category"."id",
            "field_monitoring_settings_category"."order",
            "field_monitoring_settings_category"."name",

            "field_monitoring_data_collection_activityquestionoverallfinding"."id",
            "field_monitoring_data_collection_activityquestionoverallfinding"."value",
            "field_monitoring_data_collection_activityquestionoverallfinding"."activity_question_id",

            "field_monitoring_data_collection_startedchecklist"."id",
            "field_monitoring_data_collection_startedchecklist"."information_source",
            "field_monitoring_data_collection_startedchecklist"."author_id",
            "field_monitoring_data_collection_startedchecklist"."method_id",
            "field_monitoring_data_collection_startedchecklist"."monitoring_activity_id",

            "field_monitoring_settings_method"."id",
            "field_monitoring_settings_method"."name",
            "field_monitoring_settings_method"."use_information_source",
            "field_monitoring_settings_method"."short_name"

    FROM "field_monitoring_data_collection_finding"
         INNER JOIN "field_monitoring_data_collection_activityquestion" ON ("field_monitoring_data_collection_finding"."activity_question_id" = "field_monitoring_data_collection_activityquestion"."id") INNER JOIN "field_monitoring_planning_monitoringactivity" ON ("field_monitoring_data_collection_activityquestion"."monitoring_activity_id" = "field_monitoring_planning_monitoringactivity"."id")
         LEFT OUTER JOIN "field_monitoring_settings_locationsite" ON ("field_monitoring_planning_monitoringactivity"."location_site_id" = "field_monitoring_settings_locationsite"."id")
         LEFT OUTER JOIN "locations_location" ON ("field_monitoring_planning_monitoringactivity"."location_id" = "locations_location"."id")
         INNER JOIN "field_monitoring_data_collection_startedchecklist" ON ("field_monitoring_data_collection_finding"."started_checklist_id" = "field_monitoring_data_collection_startedchecklist"."id") LEFT OUTER JOIN "partners_partnerorganization" ON ("field_monitoring_data_collection_activityquestion"."partner_id" = "partners_partnerorganization"."id")
         LEFT OUTER JOIN "reports_result" ON ("field_monitoring_data_collection_activityquestion"."cp_output_id" = "reports_result"."id") LEFT OUTER JOIN "partners_intervention" ON ("field_monitoring_data_collection_activityquestion"."intervention_id" = "partners_intervention"."id") LEFT OUTER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id") INNER JOIN "field_monitoring_settings_question" ON ("field_monitoring_data_collection_activityquestion"."question_id" = "field_monitoring_settings_question"."id") INNER JOIN "field_monitoring_settings_category" ON ("field_monitoring_settings_question"."category_id" = "field_monitoring_settings_category"."id") LEFT OUTER JOIN "field_monitoring_data_collection_activityquestionoverallfinding" ON ("field_monitoring_data_collection_activityquestion"."id" = "field_monitoring_data_collection_activityquestionoverallfinding"."activity_question_id") INNER JOIN "field_monitoring_settings_method" ON ("field_monitoring_data_collection_startedchecklist"."method_id" = "field_monitoring_settings_method"."id")
    ORDER BY "field_monitoring_data_collection_finding"."id" ASC LIMIT 66


    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_settings_question_methods"."id",
           "field_monitoring_settings_question_methods"."question_id",
           "field_monitoring_settings_question_methods"."method_id"
    FROM "field_monitoring_settings_question_methods"
    WHERE "field_monitoring_settings_question_methods"."question_id" IN (##LIST OF "field_monitoring_settings_question"."id" IN THE PAGE##);


    SELECT '##COUNTRY##' AS __schema,
            "field_monitoring_settings_option"."id",
            "field_monitoring_settings_option"."label",
            "field_monitoring_settings_option"."value",
            "field_monitoring_settings_option"."question_id"
    FROM "field_monitoring_settings_option"
    WHERE "field_monitoring_settings_option"."question_id" IN (##LIST OF "field_monitoring_settings_question"."id" IN THE PAGE##);


    SELECT "field_monitoring_data_collection_finding"."id"
    FROM "field_monitoring_data_collection_finding"
         INNER JOIN "field_monitoring_data_collection_activityquestion" ON ("field_monitoring_data_collection_finding"."activity_question_id" = "field_monitoring_data_collection_activityquestion"."id")
         INNER JOIN "field_monitoring_planning_monitoringactivity" ON ("field_monitoring_data_collection_activityquestion"."monitoring_activity_id" = "field_monitoring_planning_monitoringactivity"."id")
         LEFT OUTER JOIN "field_monitoring_settings_locationsite" ON ("field_monitoring_planning_monitoringactivity"."location_site_id" = "field_monitoring_settings_locationsite"."id")
         LEFT OUTER JOIN "locations_location" ON ("field_monitoring_planning_monitoringactivity"."location_id" = "locations_location"."id")


    """

    """Loader for FM Questions"""

    TRANSACTION_BY_BATCH = True

    def get_queryset(self):
        """
        TODO: Subquery loads db server significantly. Iterating over prefetched records to find the may be more
        scalable as it offloads processing to datamart nodes.
        """
        narrative_finding_subquery = (
            FieldMonitoringDataCollectionChecklistoverallfinding.objects.filter(
                started_checklist_id=OuterRef("started_checklist_id")
            )
            .filter(
                Q(
                    Q(partner_id=OuterRef("activity_question__partner_id"))
                    | Q(cp_output_id=OuterRef("activity_question__cp_output_id"))
                    | Q(intervention_id=OuterRef("activity_question__intervention_id"))
                )
            )
            .values("narrative_finding")[:1]
        )
        # TODO: Try to get minimum number of fields for the join operation to make query lighter
        qs = (
            self.config.source.objects.select_related(
                "activity_question",
                "activity_question__question",
                "activity_question__question__category",
                "started_checklist",
                "started_checklist__method",
                "activity_question__monitoring_activity",
                "activity_question__monitoring_activity__location",
                "activity_question__monitoring_activity__location_site",
                "activity_question__partner",
                "activity_question__partner__organization",
                "activity_question__cp_output",
                "activity_question__intervention",
                "activity_question__FieldMonitoringDataCollectionActivityquestionoverallfinding_activity_question",
            )
            .prefetch_related(
                Prefetch(
                    "activity_question__question__FieldMonitoringSettingsQuestionMethods_question",
                    queryset=FieldMonitoringSettingsQuestionMethods.objects.all(),
                    to_attr="prefetched_FieldMonitoringSettingsQuestionMethods",
                ),
                Prefetch(
                    "activity_question__question__FieldMonitoringSettingsOption_question",
                    queryset=FieldMonitoringSettingsOption.objects.all(),
                    to_attr="prefetched_FieldMonitoringSettingsOption",
                ),
            )
            .annotate(
                site_name=F("activity_question__monitoring_activity__location_site__name"),
                location_name=F("activity_question__monitoring_activity__location__name"),
                narrative_overall_finding=Subquery(narrative_finding_subquery),
                myvalue=F("value"),
            )
        )

        return qs

    def get_answer_options(
        self,
        record: FieldMonitoringDataCollectionFinding,
        values: dict,
        **kwargs,
    ):
        option_qs = record.activity_question.question.prefetched_FieldMonitoringSettingsOption
        return ", ".join([o.label for o in option_qs])

    def get_question_collection_methods(
        self,
        record: FieldMonitoringDataCollectionFinding,
        values: dict,
        **kwargs,
    ):
        methods_qs = record.activity_question.question.prefetched_FieldMonitoringSettingsQuestionMethods
        method_name_list = []

        for m in methods_qs:
            result = self.dds_field_monitoring_settings_method[
                self.dds_field_monitoring_settings_method["id"] == m.method_id
            ]["name"]

            if not result.empty:
                method_name = result.iloc[0]
                method_name_list.append(method_name)

        methods = ", ".join(method_name_list)
        return methods

    def get_overall_finding(
        self,
        record: FieldMonitoringDataCollectionFinding,
        values: dict,
        **kwargs,
    ):
        return record.narrative_overall_finding

    def populate_field_monitoring_settings_method(self):
        qs = FieldMonitoringSettingsMethod.objects.all().values("id", "name")
        self.dds_field_monitoring_settings_method = pd.DataFrame(list(qs))

    def process_country(self):
        batch_size = 2000
        logger.debug(f"Batch size:{batch_size}")

        qs = self.get_queryset()
        schema_name = self.context["country"].schema_name

        self.populate_field_monitoring_settings_method()

        paginator = DatamartPaginator(qs, batch_size)
        sid = None

        logger.debug(f"number of pages size:{len(paginator.page_range)}")

        for page_idx in paginator.page_range:
            if getattr(self, "TRANSACTION_BY_BATCH", False):
                sid = transaction.savepoint()
            try:
                page = paginator.page(page_idx)
                logger.debug(f"{page_idx} out of {len(paginator.page_range)} pages done")

                # First get all the records that currently exist to avoid get_or_create on process record
                ids_from_etools = list(page.object_list.values_list("id", flat=True))

                local_objects = self.model.objects.filter(source_id__in=ids_from_etools, schema_name=schema_name)
                local_source_ids = local_objects.values_list("source_id", flat=True)

                # figure out which ones we don't have at all locally
                to_create_remote_ids = [id for id in ids_from_etools if id not in local_source_ids]

                # figure out which ones to update:
                # this will be a list of update local objects with the new values if the local objects need updating
                # create a map in memory with source_id and record
                local_object_dict = {i.source_id: i for i in local_objects}
                to_update = []
                to_create = []

                for rec in page.object_list:
                    values = self.get_values(rec)
                    # turns out changes are detected due to the mismatch in type for dates
                    for key, value in values.items():
                        if isinstance(value, datetime.date):
                            values[key] = value.strftime("%Y-%m-%d")

                    if rec.activity_question.cp_output:
                        cp_output = rec.activity_question.cp_output
                        values["entity_type"] = "CP Output"
                        values["entity_instance"] = cp_output.name
                        values["output"] = cp_output.wbs
                    elif rec.activity_question.intervention:
                        pd = rec.activity_question.intervention
                        values["entity_type"] = "PD/SSFA"
                        values["entity_instance"] = pd.reference_number
                    elif rec.activity_question.partner:
                        partner = rec.activity_question.partner
                        values["entity_type"] = "Partner"
                        values["entity_instance"] = partner.organization.name

                    if rec.id in to_create_remote_ids:
                        new_instance = self.model(**values)
                        new_instance.source_id = rec.id
                        new_instance.schema_name = schema_name
                        to_create.append(new_instance)
                        self.increment_counter("created")
                        continue
                    else:
                        local_object_to_update = local_object_dict[rec.id]
                        if self.config.always_update or self.is_record_changed(local_object_to_update, values):
                            for field, value in values.items():
                                setattr(local_object_to_update, field, value)
                            to_update.append(local_object_to_update)
                            self.increment_counter("updated")
                        else:
                            self.increment_counter("unchanged")

                # Time to bulk_create
                self.model.objects.bulk_create(to_create)
                # time to bulk_update
                self.model.objects.bulk_update(to_update, fields=self.mapping.keys())

            except Exception:
                if sid:
                    transaction.savepoint_rollback(sid)
                raise
            else:
                if sid:
                    transaction.savepoint_commit(sid)

    def get_location(self, record: FieldMonitoringDataCollectionFinding, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Location

        loc_fields = [
            "id",
            "name",
            "p_code",
            "level",
            "source_id",
            "admin_level",
            "admin_level_name",
            "latitude",
            "longitude",
        ]

        try:
            instance = Location.objects.get(
                schema_name=self.context["country"].schema_name,
                source_id=record.activity_question.monitoring_activity.location.pk,
            )
            return {
                "id": instance.pk,
                "name": instance.name,
                "p_code": instance.p_code,
                "admin_level": instance.admin_level,
                "source_id": instance.source_id,
                "location_type": instance.admin_level_name,
                "latitude": extract_latitude(instance),
                "longitude": extract_longitude(instance),
            }
        except Location.DoesNotExist:
            return {key: "N/A" for key in loc_fields}


class FMQuestion(EtoolsDataMartModel):
    question_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(
        verbose_name=_("Question Title"),
        null=True,
        blank=True,
    )
    answer_type = models.CharField(
        verbose_name=_("Answer Type"),
        max_length=15,
        null=True,
        blank=True,
    )
    answer_options = models.TextField(
        verbose_name=_("Answer Options"),
        null=True,
        blank=True,
    )
    entity_type = models.CharField(
        verbose_name=_("Entity Type"),
        max_length=100,
        null=True,
        blank=True,
    )
    entity_instance = models.CharField(
        verbose_name=_("Entity Instance"),
        max_length=255,
        null=True,
        blank=True,
    )
    vendor_number = models.CharField(max_length=30, blank=True, null=True)
    reference_number = models.CharField(max_length=100, null=True)
    output = models.CharField(
        verbose_name=_("Output WBS"),
        max_length=50,
        null=True,
        blank=True,
    )
    question_collection_methods = models.TextField(
        verbose_name=_("Question Collection Methods"),
        null=True,
        blank=True,
    )
    collection_method = models.CharField(
        verbose_name=_("Collection Method"),
        max_length=100,
        null=True,
        blank=True,
    )
    answer = JSONField(
        verbose_name=_("Answer"),
        null=True,
        blank=True,
    )
    summary_answer = JSONField(
        verbose_name=_("Summary Answer"),
        null=True,
        blank=True,
    )
    overall_finding = JSONField(
        verbose_name=_("Overall Finding"),
        null=True,
        blank=True,
    )
    monitoring_activity_id = models.IntegerField(
        verbose_name=_("Monitoring Activity ID"),
        null=True,
        blank=True,
    )
    monitoring_activity = models.CharField(
        verbose_name=_("Monitoring Activity"),
        max_length=64,
        blank=True,
        null=True,
    )
    specific_details = models.TextField(
        verbose_name=_("Specific Details"),
        null=True,
        blank=True,
    )
    date_of_capture = models.CharField(
        verbose_name=_("Date of Capture"),
        max_length=50,
        null=True,
        blank=True,
    )
    monitoring_activity_end_date = models.CharField(
        verbose_name=_("Monitoring Activity End Date"),
        max_length=50,
        null=True,
        blank=True,
    )
    location = JSONField(blank=True, null=True, default=dict)
    site = models.CharField(
        verbose_name=_("Location"),
        max_length=254,
        null=True,
        blank=True,
    )
    category = models.CharField(max_length=100, null=True, blank=True)
    information_source = models.CharField(max_length=100, null=True, blank=True)
    is_hact = models.BooleanField(null=True, blank=True)

    loader = FMQuestionLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionFinding
        depends_as_str = ("etools_datamart.apps.mart.data.models.Location",)
        mapping = dict(
            question_id="id",
            title="activity_question.question.text",
            answer_type="activity_question.question.answer_type",
            answer_options="-",
            entity_type="i",
            entity_instance="i",
            vendor_number="activity_question.partner.organization.vendor_number",
            reference_number="activity_question.intervention.reference_number",
            question_collection_methods="-",
            collection_method="started_checklist.method.name",
            answer="value",
            summary_answer="activity_question.FieldMonitoringDataCollectionActivityquestionoverallfinding_activity_question.value",
            overall_finding="narrative_overall_finding",
            monitoring_activity_id="activity_question.monitoring_activity.pk",
            monitoring_activity="activity_question.monitoring_activity.number",
            specific_details="i",
            date_of_capture="",
            monitoring_activity_end_date="activity_question.monitoring_activity.end_date",
            location="-",
            site="site_name",
            # site="activity_question.monitoring_activity.location_site.name",
            category="activity_question.question.category.name",
            information_source="started_checklist.information_source",
            is_hact="activity_question.question.is_hact",
        )


class FMOntrackLoader(EtoolsLoader):
    """Loader for FM Ontrack"""

    """
    --
    SET search_path = public,##COUNTRY##
    --
    SELECT COUNT(*) AS "__count"
    FROM "field_monitoring_data_collection_activityoverallfinding";
    
    --
    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_data_collection_activityoverallfinding"."id",
           "field_monitoring_data_collection_activityoverallfinding"."narrative_finding",
           "field_monitoring_data_collection_activityoverallfinding"."on_track",
           "field_monitoring_data_collection_activityoverallfinding"."cp_output_id",
           "field_monitoring_data_collection_activityoverallfinding"."intervention_id",
           "field_monitoring_data_collection_activityoverallfinding"."monitoring_activity_id",
           "field_monitoring_data_collection_activityoverallfinding"."partner_id"
    FROM "field_monitoring_data_collection_activityoverallfinding"
    ORDER BY "field_monitoring_data_collection_activityoverallfinding"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

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
           "field_monitoring_planning_monitoringactivity"."number"
    FROM "field_monitoring_planning_monitoringactivity"
    WHERE "field_monitoring_planning_monitoringactivity"."id"
    IN (## LIST OF "field_monitoring_data_collection_activityoverallfinding"."monitoring_activity_id" in the page##);
    
    --
    SELECT '##COUNTRY##' AS __schema,
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
    WHERE "locations_location"."id" 
    IN(## LIST OF field_monitoring_planning_monitoringactivity"."location_id" in the page##);

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
           "partners_partnerorganization"."organization_id" 
    FROM "partners_partnerorganization" 
    WHERE "partners_partnerorganization"."id" IN (## ##);


    """

    def get_overall_finding_rating(
        self,
        record: FieldMonitoringDataCollectionActivityoverallfinding,
        values: dict,
        **kwargs,
    ):
        return "On track" if record.on_track else "Off track"

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.get_queryset()

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for rec in page.object_list:
                filters = self.config.key(self, rec)
                values = self.get_values(rec)
                if rec.cp_output:
                    values["entity"] = rec.cp_output.name
                    values["outcome"] = rec.cp_output.parent.wbs if rec.cp_output.parent else None
                    values["output"] = rec.cp_output.wbs
                    values["programme_areas"] = (
                        f"{rec.cp_output.programme_area_code} {rec.cp_output.programme_area_name}"
                    )
                    values["entity_type"] = "CP Output"
                elif rec.intervention:
                    values["entity"] = rec.intervention.reference_number
                    values["outcome"] = None
                    values["output"] = None
                    values["programme_areas"] = None
                    values["entity_type"] = "PD/SSFA"
                elif rec.partner:
                    values["entity"] = rec.partner.organization.name
                    values["outcome"] = None
                    values["output"] = None
                    values["programme_areas"] = None
                    values["entity_type"] = "Partner"
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def get_sections(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        data = []
        qs = ReportsSector.objects.filter(
            FieldMonitoringPlanningMonitoringactivitySections_section__monitoringactivity=record.monitoring_activity
        )
        for rec in qs:
            data.append(
                dict(
                    source_id=rec.pk,
                    name=rec.name,
                    description=rec.description,
                ),
            )
        values["sections_data"] = data
        return ", ".join([sec["name"] for sec in data])

    def get_field_offices(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        activity = record.monitoring_activity
        return list(
            activity.FieldMonitoringPlanningMonitoringactivityOffices_monitoringactivity.values_list(
                "office__name", flat=True
            )
        )

    def get_location(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Location

        loc_fields = [
            "id",
            "name",
            "p_code",
            "level",
            "source_id",
            "admin_level",
            "admin_level_name",
            "latitude",
            "longitude",
        ]

        try:
            instance = Location.objects.get(
                schema_name=self.context["country"].schema_name, source_id=record.monitoring_activity.location.pk
            )
            return {
                "id": instance.pk,
                "name": instance.name,
                "p_code": instance.p_code,
                "admin_level": instance.admin_level,
                "source_id": instance.source_id,
                "location_type": instance.admin_level_name,
                "latitude": extract_latitude(instance),
                "longitude": extract_longitude(instance),
            }
        except Location.DoesNotExist:
            return {key: "N/A" for key in loc_fields}

    def get_team_members(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        return ", ".join(
            record.monitoring_activity.FieldMonitoringPlanningMonitoringactivityTeamMembers_monitoringactivity.values_list(
                "user__email", flat=True
            )
        )


class FMOntrack(EtoolsDataMartModel):
    entity = models.CharField(
        verbose_name=_("Entity"),
        max_length=255,
        null=True,
        blank=True,
    )
    entity_type = models.CharField(
        verbose_name=_("Entity Type"),
        max_length=100,
        null=True,
        blank=True,
    )
    narrative_finding = models.TextField(
        verbose_name=_("Overall Finding Narrative"),
        null=True,
        blank=True,
    )
    overall_finding_rating = models.CharField(
        verbose_name=_("Overall Finding Narrative"),
        max_length=50,
        null=True,
        blank=True,
    )
    monitoring_activity = models.CharField(
        verbose_name=_("Monitoring Activity"),
        max_length=64,
        blank=True,
        null=True,
    )
    monitoring_activity_id = models.IntegerField(
        verbose_name=_("Monitoring Activity ID"),
        null=True,
        blank=True,
    )
    monitoring_activity_end_date = models.CharField(
        verbose_name=_("Monitoring Activity End Date"),
        max_length=50,
        null=True,
        blank=True,
    )
    location = JSONField(blank=True, null=True, default=dict)
    site = models.CharField(
        verbose_name=_("Location"),
        max_length=254,
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, null=True, blank=True)
    outcome = models.CharField(
        verbose_name=_("Outcome WBS"),
        max_length=30,
        null=True,
        blank=True,
    )
    output = models.CharField(
        verbose_name=_("Output WBS"),
        max_length=50,
        null=True,
        blank=True,
    )
    programme_areas = models.TextField(
        verbose_name=_("Programme Areas"),
        null=True,
        blank=True,
    )
    vendor_number = models.CharField(max_length=30, blank=True, null=True)
    reference_number = models.CharField(max_length=100, null=True)
    field_offices = JSONField(blank=True, null=True, default=dict)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    person_responsible_email = models.CharField(max_length=254, null=True, blank=True)
    team_members = models.TextField(blank=True, null=True)

    loader = FMOntrackLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionActivityoverallfinding
        depends_as_str = ("etools_datamart.apps.mart.data.models.Location",)
        mapping = dict(
            entity="i",
            entity_type="i",
            overall_finding_rating="-",
            monitoring_activity="monitoring_activity.number",
            monitoring_activity_id="monitoring_activity.pk",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="-",
            site="monitoring_activity.locationsite.name",
            status="monitoring_activity.status",
            outcome="i",
            output="i",
            programme_areas="i",
            vendor_number="partner.organization.vendor_number",
            reference_number="intervention.reference_number",
            sections="-",
            person_responsible_email="monitoring_activity.visit_lead.email",
            team_members="-",
        )


"""
Queries for Loader:   
  
  
  
  ===FieldMonitoringSettingsOption

"""


class FMOptions(EtoolsDataMartModel):
    label = models.CharField(max_length=100, null=True, blank=True)
    option_value = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    question_id = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100)
    is_custom = models.BooleanField(default=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)

    loader = EtoolsLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringSettingsOption
        mapping = dict(
            question="question.text",
            question_id="question.id",
            category="question.category.name",
            is_custom="question.is_custom",
            is_active="question.is_active",
            option_value="value",
        )
