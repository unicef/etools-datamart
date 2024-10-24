from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts

from ..common import DataMartViewSet


class EngagementSerializerSimple(DataMartSerializer):
    partner = serializers.IntegerField(source="partner.id")
    schema = serializers.CharField(source="schema_name")

    class Meta(DataMartSerializer.Meta):
        model = models.Engagement
        exclude = None
        fields = (
            "country_name",
            "schema",
            "created",
            "modified",
            "reference_number",
            "status",
            "partner_contacted_at",
            "engagement_type",
            "start_date",
            "end_date",
            "total_value",
            "date_of_field_visit",
            "date_of_draft_report_to_ip",
            "date_of_comments_by_ip",
            "date_of_draft_report_to_unicef",
            "date_of_comments_by_unicef",
            "date_of_report_submit",
            "date_of_final_report",
            "date_of_cancel",
            "amount_refunded",
            "additional_supporting_documentation_provided",
            "justification_provided_and_accepted",
            "write_off_required",
            "cancel_comment",
            "explanation_for_additional_information",
            "joint_audit",
            "shared_ip_with",
            "exchange_rate",
            "partner",
            "agreement",
            "po_item",
        )


URL_MAP = {
    models.Engagement.TYPE_AUDIT: "audit",
    models.Engagement.TYPE_MICRO_ASSESSMENT: "micro-assessments",
    models.Engagement.TYPE_SPOT_CHECK: "spot-checks",
    models.Engagement.TYPE_SPECIAL_AUDIT: "special-audits",
}


class EngagementSerializer(DataMartSerializer):
    partner_name = serializers.SerializerMethodField()
    partner_code = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.Engagement
        exclude = (
            "seen",
            "source_id",
        )

    def get_url(self, obj):
        try:
            return "%s/ap/%s/%s/overview" % (config.ETOOLS_ADDRESS, URL_MAP[obj.engagement_type], obj.source_id)
        except KeyError:
            return ""

    def get_partner_name(self, obj):
        try:
            return obj.partner["name"]
        except KeyError:
            return "N/A"

    def get_partner_code(self, obj):
        try:
            return obj.partner["vendor_number"]
        except KeyError:
            return "N/A"


class EngagementDetailSerializer(DataMartSerializer):
    partner = serializers.SerializerMethodField()
    vendor_number = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.Engagement
        exclude = None
        fields = (
            "po_item",
            "engagement_type",
            "start_date",
            "end_date",
            "partner",
            "partner_contacted_at",
            "vendor_number",
            "auditor",
            "total_value",  # Value of FACE forms
            "spotcheck_total_amount_tested",
            "date_of_field_visit",  # FACE Form period
            "final_report",  # Findings
            "agreement",  # Agreed actions by partner
            "rating",
            "rating_extra",
            "spotcheck_total_amount_of_ineligible_expenditure",
            "financial_findings",  # Financial findings
            "action_points",
            "status",
            "audit_opinion",
        )

    def get_partner(self, obj):
        try:
            return obj.partner["name"]
        except KeyError:
            return "N/A"

    def get_vendor_number(self, obj):
        try:
            return obj.partner["vendor_number"]
        except KeyError:
            return "N/A"


class EngagementFilterForm(forms.Form):
    engagement_type__in = Select2MultipleChoiceField(
        label="Engagement Type", choices=models.Engagement.TYPES, required=False
    )
    partner_contacted_at = DateRangePickerField(label="Date IP was contacted", required=False)

    start_date = DateRangePickerField(label="Start Date", required=False)

    end_date = DateRangePickerField(label="End Date", required=False)

    status__in = Select2MultipleChoiceField(
        label="Status", choices=AuditEngagementConsts.DISPLAY_STATUSES, required=False
    )

    audit_opinion__in = Select2MultipleChoiceField(
        label="Audit Opinion", choices=models.Engagement.AUDIT_OPTIONS, required=False
    )

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if "status__in" in filters:
            filters.setlist("status__in", data["status__in"].split(","))
        if "engagement_type__in" in filters:
            filters.setlist("engagement_type__in", data["engagement_type__in"].split(","))
        if "audit_opinion__in" in filters:
            filters.setlist("audit_opinion__in", data["audit_opinion__in"].split(","))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class EngagementViewSet(DataMartViewSet):
    querystringfilter_form_base_class = EngagementFilterForm

    serializer_class = EngagementSerializer
    queryset = models.Engagement.objects.all()
    filter_fields = ("engagement_type", "partner_contacted_at", "start_date", "end_date", "status", "audit_opinion")
    serializers_fieldsets = {"std": None, "simple": EngagementSerializerSimple}

    def get_querystringfilter_form(self, request, filter):
        return EngagementFilterForm(request.GET, filter.form_prefix)


class EngagementDetailViewSet(DataMartViewSet):
    querystringfilter_form_base_class = EngagementFilterForm

    serializer_class = EngagementDetailSerializer
    queryset = models.Engagement.objects.all()
    filter_fields = ("engagement_type", "partner_contacted_at", "start_date", "end_date", "status", "audit_opinion")
    serializers_fieldsets = {"std": None, "simple": EngagementSerializerSimple}

    def get_querystringfilter_form(self, request, filter):
        return EngagementFilterForm(request.GET, filter.form_prefix)
