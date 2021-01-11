from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import (
    FieldMonitoringDataCollectionActivityoverallfinding,
    FieldMonitoringDataCollectionFinding,
    FieldMonitoringPlanningMonitoringactivityCpOutputs,
    FieldMonitoringPlanningMonitoringactivityInterventions,
    FieldMonitoringPlanningMonitoringactivityPartners,
    FieldMonitoringSettingsOption,
    FieldMonitoringSettingsQuestionMethods,
)


class FMQuestionLoader(EtoolsLoader):
    """Loader for FM Questions"""
    def get_answer_options(
            self,
            record: FieldMonitoringDataCollectionFinding,
            values: dict,
            **kwargs,
    ):
        option_qs = FieldMonitoringSettingsOption.objects.filter(
            question=record.activity_question.question,
        )
        return ", ".join([o.label for o in option_qs.all()])

    def get_question_collection_methods(
            self,
            record: FieldMonitoringDataCollectionFinding,
            values: dict,
            **kwargs,
    ):
        methods_qs = FieldMonitoringSettingsQuestionMethods.objects.filter(
            question=record.activity_question.question,
        )
        return ", ".join(
            [m.method.name for m in methods_qs.all()]
        )

    def process_country(self):
        for rec in self.get_queryset():
            filters = self.config.key(self, rec)
            values = self.get_values(rec)
            activity = rec.activity_question.monitoring_activity
            partner_qs = FieldMonitoringPlanningMonitoringactivityPartners.objects.filter(
                monitoringactivity=activity,
            )
            intervention_qs = FieldMonitoringPlanningMonitoringactivityInterventions.objects.filter(
                monitoringactivity=activity,
            )
            cp_output_qs = FieldMonitoringPlanningMonitoringactivityCpOutputs.objects.filter(
                monitoringactivity=activity,
            )
            for rec in partner_qs.all():
                partner = rec.partnerorganization
                values["entity_type"] = "Partner"
                values["entity_instance"] = partner.name
                op = self.process_record(filters, values)
                self.increment_counter(op)
            for rec in intervention_qs.all():
                pd = rec.intervention
                values["entity_type"] = "PD/SSFA"
                values["entity_instance"] = pd.reference_number
                op = self.process_record(filters, values)
                self.increment_counter(op)
            for rec in cp_output_qs.all():
                cp_ouput = rec.result
                values["entity_type"] = "CP Output"
                values["entity_instance"] = cp_output.name
                op = self.process_record(filters, values)
                self.increment_counter(op)


class FMQuestion(EtoolsDataMartModel):
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
    monitoring_activity_id = models.IntegerField(
        verbose_name=_("Monitoring Activity ID"),
        null=True,
        blank=True,
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
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=254,
        null=True,
        blank=True,
    )
    site = models.CharField(
        verbose_name=_("Location"),
        max_length=254,
        null=True,
        blank=True,
    )

    loader = FMQuestionLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionFinding
        mapping = dict(
            title="activity_question.text",
            answer_type="activity_question.answer_type",
            answer_options="-",
            entity_type="i",
            entity_instance="i",
            question_collection_methods="-",
            collection_method="started_checklist.method",
            answer="value",
            summary_answer="activity_question.overall_finding.value",
            monitoring_activity_id="activity_question.monitoring_activity.pk",
            specific_details="i",
            date_of_capture="",
            monitoring_activity_end_date="activity_question.monitoring_activity.end_date",
            location="activity_question.monitoring_activity.location.name",
            site="activity_question.monitoring_activity.locationsite.name",
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
        for rec in self.get_queryset():
            filters = self.config.key(self, rec)
            values = self.get_values(rec)
            activity = rec.monitoring_activity
            partner_qs = FieldMonitoringPlanningMonitoringactivityPartners.objects.filter(
                monitoringactivity=activity,
            )
            intervention_qs = FieldMonitoringPlanningMonitoringactivityInterventions.objects.filter(
                monitoringactivity=activity,
            )
            cp_output_qs = FieldMonitoringPlanningMonitoringactivityCpOutputs.objects.filter(
                monitoringactivity=activity,
            )
            for rec in partner_qs.all():
                values["entity"] = rec.partnerorganization.name
                values["outcome"] = None
                op = self.process_record(filters, values)
                self.increment_counter(op)
            for rec in intervention_qs.all():
                values["entity"] = rec.intervention.reference_number
                values["outcome"] = None
                op = self.process_record(filters, values)
                self.increment_counter(op)
            for rec in cp_output_qs.all():
                cp_output = rec.result
                values["entity"] = cp_output.name
                values["outcome"] = cp_output.parent.wbs if cp_output.parent else None
                op = self.process_record(filters, values)
                self.increment_counter(op)


class FMOntrack(EtoolsDataMartModel):
    entity = models.CharField(
        verbose_name=_("Entity"),
        max_length=255,
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
    monitoring_activity_end_date = models.CharField(
        verbose_name=_("Monitoring Activity End Date"),
        max_length=50,
        null=True,
        blank=True,
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=254,
        null=True,
        blank=True,
    )
    site = models.CharField(
        verbose_name=_("Location"),
        max_length=254,
        null=True,
        blank=True,
    )
    outcome = models.CharField(
        verbose_name=_("Outcome WBS"),
        max_length=30,
        null=True,
        blank=True,
    )

    loader = FMOntrackLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionActivityoverallfinding
        mapping = dict(
            entity="i",
            narrative_finding="i",
            overall_finding_rating="-",
            monitoring_activity="monitoring_activity.number",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="monitoring_activity.location.name",
            site="monitoring_activity.locationsite.name",
            outcome="i",
        )
