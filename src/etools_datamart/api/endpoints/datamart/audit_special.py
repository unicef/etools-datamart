from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from ..common import DataMartViewSet


class AuditSpecialSerializer(DataMartSerializer):
    partner_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.AuditSpecial
        exclude = (
            "seen",
            "source_id",
        )

    def get_url(self, obj):
        try:
            return "{}/ap/special-audits/{}/overview".format(
                config.ETOOLS_ADDRESS,
                obj.source_id,
            )
        except KeyError:
            return ""

    def get_partner_name(self, obj):
        try:
            return obj.partner["name"]
        except KeyError:
            return "N/A"


class AuditSpecialFilterForm(forms.Form):
    date_of_field_visit = DateRangePickerField(
        label="Date of Field Visit",
        required=False,
    )
    date_of_final_report = DateRangePickerField(
        label="Date of Final Report",
        required=False,
    )


class AuditSpecialViewSet(DataMartViewSet):
    querystringfilter_form_base_class = AuditSpecialFilterForm

    serializer_class = AuditSpecialSerializer
    queryset = models.AuditSpecial.objects.all()
    filter_fields = (
        "date_of_field_visit",
        "date_of_final_report",
    )

    def get_querystringfilter_form(self, request, filter):
        return AuditSpecialFilterForm(request.GET, filter.form_prefix)
