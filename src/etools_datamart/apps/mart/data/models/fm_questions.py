from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext as _

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import (
    FieldMonitoringDataCollectionActivityoverallfinding,
    FieldMonitoringDataCollectionChecklistoverallfinding,
    FieldMonitoringDataCollectionFinding,
    FieldMonitoringSettingsOption,
    FieldMonitoringSettingsQuestionMethods,
    ReportsSector,
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

    # def get_summary_answer(
    #         self,
    #         record: FieldMonitoringDataCollectionFinding,
    #         values: dict,
    #         **kwargs,
    # ):
    #     overall_finding = FieldMonitoringDataCollectionActivityoverallfinding.objects.filter(
    #         partner=record.activity_question.partner,
    #         intervention=record.activity_question.intervention,
    #         cp_output=record.activity_question.cp_output,
    #         monitoring_activity=record.activity_question.monitoring_activity
    #     ).first()
    #     return getattr(overall_finding, 'narrative_finding', None)

    def get_overall_finding(
            self,
            record: FieldMonitoringDataCollectionFinding,
            values: dict,
            **kwargs,
    ):
        checklist_finding = FieldMonitoringDataCollectionChecklistoverallfinding.objects.filter(
            partner=record.activity_question.partner,
            intervention=record.activity_question.intervention,
            cp_output=record.activity_question.cp_output,
            started_checklist=record.started_checklist).first()
        return getattr(checklist_finding, 'narrative_finding', None)

    def process_country(self):
        for rec in self.get_queryset():
            filters = self.config.key(self, rec)
            values = self.get_values(rec)
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
                values["entity_instance"] = partner.name
            op = self.process_record(filters, values)
            self.increment_counter(op)

    def get_location(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Location
        loc_fields = ['id', 'name', 'p_code', 'level', 'source_id', 'admin_level', 'admin_level_name',
                      'latitude', 'longitude']

        try:
            instance = Location.objects.get(
                schema_name=self.context['country'].schema_name,
                source_id=record.activity_question.monitoring_activity.pk
            )
            return {
                'id': instance.pk,
                'name': instance.name,
                'p_code': instance.p_code,
                'admin_level': instance.admin_level,
                'source_id': instance.source_id,
                'location_type': instance.admin_level_name,
                'latitude': instance.latitude,
                'longitude': instance.longitude,
            }
        except Location.DoesNotExist:
            return {key: 'N/A' for key in loc_fields}


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
        mapping = dict(
            title="activity_question.question.text",
            answer_type="activity_question.question.answer_type",
            answer_options="-",
            entity_type="i",
            entity_instance="i",
            vendor_number="activity_question.partner.vendor_number",
            reference_number='activity_question.intervention.reference_number',
            question_collection_methods="-",
            collection_method="started_checklist.method.name",
            answer="value",
            summary_answer="activity_question.FieldMonitoringDataCollectionActivityquestionoverallfinding_activity_question.value",
            overall_finding="-",
            monitoring_activity_id="activity_question.monitoring_activity.pk",
            monitoring_activity="activity_question.monitoring_activity.number",
            specific_details="i",
            date_of_capture="",
            monitoring_activity_end_date="activity_question.monitoring_activity.end_date",
            location="-",
            site="activity_question.monitoring_activity.locationsite.name",
            category='activity_question.question.category.name',
            information_source='started_checklist.information_source',
            is_hact='activity_question.question.is_hact',
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
            if rec.cp_output:
                values["entity"] = rec.cp_output.name
                values["outcome"] = rec.cp_output.parent.wbs if rec.cp_output.parent else None
                values["output"] = rec.cp_output.wbs
                values["programme_areas"] = f'{rec.cp_output.programme_area_code} {rec.cp_output.programme_area_name}'
                values["entity_type"] = "CP Output"
            elif rec.intervention:
                values["entity"] = rec.intervention.reference_number
                values["outcome"] = None
                values["output"] = None
                values["programme_areas"] = None
                values["entity_type"] = "PD/SSFA"
            elif rec.partner:
                values["entity"] = rec.partner.name
                values["outcome"] = None
                values["output"] = None
                values["programme_areas"] = None
                values["entity_type"] = "Partner"
            op = self.process_record(filters, values)
            self.increment_counter(op)

    def get_sections(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        data = []
        qs = ReportsSector.objects.filter(
            FieldMonitoringPlanningMonitoringactivitySections_section__monitoringactivity=record.monitoring_activity)
        for rec in qs:
            data.append(
                dict(
                    source_id=rec.pk,
                    name=rec.name,
                    description=rec.description,
                ),
            )
        values['sections_data'] = data
        return ", ".join([sec['name'] for sec in data])

    def get_location(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Location
        loc_fields = ['id', 'name', 'p_code', 'level', 'source_id', 'admin_level', 'admin_level_name',
                      'latitude', 'longitude']

        try:
            instance = Location.objects.get(
                schema_name=self.context['country'].schema_name,
                source_id=record.monitoring_activity.pk
            )
            return {
                'id': instance.pk,
                'name': instance.name,
                'p_code': instance.p_code,
                'admin_level': instance.admin_level,
                'source_id': instance.source_id,
                'location_type': instance.admin_level_name,
                'latitude': instance.latitude,
                'longitude': instance.longitude,
            }
        except Location.DoesNotExist:
            return {key: 'N/A' for key in loc_fields}

    def get_team_members(self, record: FieldMonitoringDataCollectionActivityoverallfinding, values: dict, **kwargs):
        return ', '.join(record.monitoring_activity.
                         FieldMonitoringPlanningMonitoringactivityTeamMembers_monitoringactivity.values_list(
            'user__email', flat=True))


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
    field_office = models.CharField(max_length=254, blank=True, null=True)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    person_responsible_email = models.CharField(max_length=254, null=True, blank=True)
    team_members = models.TextField(blank=True, null=True)

    loader = FMOntrackLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionActivityoverallfinding
        mapping = dict(
            entity="i",
            entity_type="i",
            overall_finding_rating="-",
            monitoring_activity="monitoring_activity.number",
            monitoring_activity_id="monitoring_activity.pk",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="-",
            site="monitoring_activity.locationsite.name",
            status='monitoring_activity.status',
            outcome="i",
            output="i",
            programme_areas="i",
            vendor_number="partner.vendor_number",
            reference_number='intervention.reference_number',
            field_office='monitoring_activity.field_office.name',
            sections="-",
            person_responsible_email="monitoring_activity.visit_lead.email",
            team_members='-',
        )


class FMOptions(EtoolsDataMartModel):
    label = models.CharField(max_length=50, null=True, blank=True)
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
            option_value='value'
        )
