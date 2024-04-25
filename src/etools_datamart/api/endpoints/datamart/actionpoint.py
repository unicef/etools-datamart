from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import CleareableSelect2ChoiceField, DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common

URLMAP = {
    "AuditSpotcheck": "%s/ap/spot-checks/%s/overview/?schema=%s",
    "AuditMicroassessment": "%s/ap/micro-assessments/%s/overview/?schema=%s",
    "AuditSpecialaudit": "%s/ap/special-audits/%s/overview/?schema=%s",
    "AuditAudit": "%s/ap/audits/%s/overview/?schema=%s",
    "TpmTpmactivity": "%s/t2f/edit-travel/%s/?schema=%s",
    "T2FTravelactivity": "%s/t2f/edit-travel/%s/?schema=%s",
    "PseaAssessment": "%s/psea/assessments/%s/details/?schema=%s",
    "FieldMonitoringPlanningMonitoringactivity": "%s/fm/activities/%s/details/?schema=%s",
}


MODULEMAP = {
    "AuditSpotcheck": "fam",
    "AuditMicroassessment": "fam",
    "AuditSpecialaudit": "fam",
    "AuditAudit": "fam",
    "TpmTpmactivity": "tpm",
    "T2FTravelactivity": "trips",
    "PseaAssessment": "psea",
    "FieldMonitoringPlanningMonitoringactivity": "fm",
}


class UrlsMixin(DataMartSerializer):
    related_module_url = serializers.SerializerMethodField()
    related_module = serializers.SerializerMethodField()

    def get_related_module(self, obj):
        if obj.related_module_class and obj.related_module_id:
            return MODULEMAP[obj.related_module_class]

    def get_related_module_url(self, obj):
        if obj.related_module_class and obj.related_module_id:
            base_url = URLMAP[obj.related_module_class]
            return base_url % (config.ETOOLS_ADDRESS, obj.related_module_id, obj.schema_name)


class ActionPointSerializerV2(UrlsMixin, DataMartSerializer):
    section = serializers.CharField(source="section_type")
    pd_ssfa_title = serializers.CharField(source="intervention_title")
    pd_ssfa_reference_number = serializers.CharField(source="intervention_title")
    fam_category = serializers.CharField(source="category_description")
    action_point_url = serializers.SerializerMethodField()

    def get_action_point_url(self, obj):
        return "%s/apd/action-points/detail/%s/?schema=%s" % (config.ETOOLS_ADDRESS, obj.source_id, obj.schema_name)

    class Meta(DataMartSerializer.Meta):
        model = models.ActionPoint
        exclude = None
        fields = (
            "reference_number",
            "created",
            "status",
            "assigned_by_name",
            "assigned_by_email",
            "assigned_to_name",
            "assigned_to_email",
            "office",
            "section",
            "due_date",
            "date_of_completion",
            "high_priority",
            "description",
            "actions_taken",
            "country_name",
            "area_code",
            "location_name",
            "location_pcode",
            "location_level",
            "location_levelname",
            "partner_name",
            "vendor_number",
            "cp_output",
            "cp_output_id",
            "pd_ssfa_title",
            "pd_ssfa_reference_number",
            "category_module",
            "module_reference_number",
            "module_task_activity_reference_number",
            "fam_category",
            "related_module",
            "related_module_class",
            "related_module_url",
            "action_point_url",
        )


class ActionPointSerializer(UrlsMixin, DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.ActionPoint
        exclude = ()


class ActionPointSimpleSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.ActionPoint
        exclude = None
        fields = (
            "actions_taken",
            "assigned_by_name",
            "assigned_by_email",
            "assigned_to_name",
            "assigned_to_email",
            "status",
        )


class ActionPointFilterForm(forms.Form):
    created = DateRangePickerField(label="Created between", required=False)

    date_of_completion = DateRangePickerField(label="Date of completion", required=False)

    due_date = DateRangePickerField(label="Due Date", required=False)

    high_priority = CleareableSelect2ChoiceField(
        required=False,
        choices=(
            (None, "All"),
            (False, "False"),
            (True, "True"),
        ),
    )

    status = CleareableSelect2ChoiceField(
        label="Status",
        required=False,
        choices=(
            ('open', "Open"),
            ('completed', "Completed'"),
        ),
    ))


class ActionPointViewSet(common.DataMartViewSet):
    serializer_class = ActionPointSerializer
    queryset = models.ActionPoint.objects.all()
    filter_fields = ("created", "date_of_completion", "due_date", "high_priority", "status")
    serializers_fieldsets = {"std": ActionPointSerializer, "v2": ActionPointSerializerV2}
    querystringfilter_form_base_class = ActionPointFilterForm

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
