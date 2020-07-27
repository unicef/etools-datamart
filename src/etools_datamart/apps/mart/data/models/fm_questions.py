from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel


class FMQuestionLoader(EtoolsLoader):
    """Loader for FM Questions"""
    def get_answer_options(
            self,
            record: FieldMonitoringDataCollectionActivityquestion,
            values: dict,
            **kwargs,
    ):
        return ", ".join([o.label for o in question.options.all()])

    def get_question_collection_methods(
            self,
            record: FieldMonitoringDataCollectionActivityquestion,
            values: dict,
            **kwargs,
    ):
        return ", ".join([m.name for m in question.methods.all()])

    def get_action_point(
            self,
            record: FieldMonitoringDataCollectionActivityquestion,
            values: dict,
            **kwargs,
    ):
        try:
            action_point = ActionPoint.objects.filter(
                monitoring_activity=record.monitoring_activity,
            )
        except ActionPoint.DoesNotExist:
            date_of_capture = None
            location = None
        except ActionPoint.MultipleResults:
            # TODO find out what should happen in this scenario
            date_of_capture = None
            location = None
        else:
            date_of_capture = action_point.date_of_completion
            location = action_point.location
        values["date_of_capture"] = date_of_capture
        return action_point


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
    entity_type = models.CharField()
    entity_instance = models.CharField()
    question_collection_methods = models.TextField(
        verbose_name=_("Question Collection Methods"),
        null=True,
        blank=True,
    )
    collection_method = models.CharField()
    answer = models.CharField()
    summary_answer = models.CharField()
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
        source = FieldMonitoringDataCollectionActivityquestion
        mapping = add_location_mapping(dict(
            title="question.text",
            answer_type="question.answer_type",
            answer_options="-",
            entity_type="",
            entity_instance="",
            question_collection_methods="-",
            collection_method="",
            answer="",
            summary_answer="",
            monitoring_activity_id="monitoring_activity.pk",
            specific_details="i",
            date_of_capture="i",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="monitoring_activity.location.name",
            site="monitoring_activity.locationsite.name",
        ))


class FMOntrackLoader():
    """Loader for FM Ontrack"""
    def get_overall_finding_rating(
            self,
            record: FieldMonitoringDataCollectionChecklistoverallfinding,
            values: dict,
            **kwargs,
    ):
        return "On track" if record.on_track else "Off track"

    def get_outcome(
            self,
            record: FieldMonitoringDataCollectionChecklistoverallfinding,
            values: dict,
            **kwargs,
    ):
        return ", ".join([r.wbs for r in record.cp_outputs.all()])


class FMOntrack(EtoolsDataMartModel):
    entity = models.CharField()
    overall_finding_narrative = models.TextField(
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
        null=True,
        blank=True,
    )

    loader = FMOntrackLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionChecklistoverallfinding
        mapping = add_location_mapping(dict(
            entity="",
            overall_finding_narrative="i",
            overall_finding_rating="-",
            monitoring_activity="monitoring_activity.number",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="monitoring_activity.location.name",
            site="monitoring_activity.locationsite.name",
            outcome="-",
        ))
