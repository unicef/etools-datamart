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
