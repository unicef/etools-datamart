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
            date_of_capture="",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="monitoring_activity.location.name",
            site="monitoring_activity.locationsite.name",
        ))


class FMOntrackLoader(EtoolsLoader):
    """Loader for FM Ontrack"""
    def get_overall_finding_rating(
            self,
            record: FieldMonitoringDataCollectionActivityoverallfinding,
            values: dict,
            **kwargs,
    ):
        return "On track" if record.on_track else "Off track"

    def get_outcome(
            self,
            record: FieldMonitoringDataCollectionActivityoverallfinding,
            values: dict,
            **kwargs,
    ):
        # Needs to be from monitoring activity if entity output grab parent
        if not record.monitoring_activity.cp_outputs.exist():
            return None
        return ", ".join([
            r.parent.wbs for r in record.monitoring_activity.cp_outputs.all()
            if r.parent
        ])


class FMOntrack(EtoolsDataMartModel):
    entity = models.CharField()
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
        null=True,
        blank=True,
    )

    loader = FMOntrackLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = FieldMonitoringDataCollectionActivityoverallfinding
        mapping = add_location_mapping(dict(
            entity="",
            narrative_finding="i",
            overall_finding_rating="-",
            monitoring_activity="monitoring_activity.number",
            monitoring_activity_end_date="monitoring_activity.end_date",
            location="monitoring_activity.location.name",
            site="monitoring_activity.locationsite.name",
            outcome="-",
        ))
