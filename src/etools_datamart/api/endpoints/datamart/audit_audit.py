from django import forms

from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts

from ..common import DataMartViewSet


class AuditSerializer(DataMartSerializer):
    partner_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.Audit
        exclude = ('seen', 'source_id',)

    def get_url(self, obj):
        try:
            return "{}/ap/audits/{}/overview".format(
                config.ETOOLS_ADDRESS,
                obj.source_id,
            )
        except KeyError:
            return ""

    def get_partner_name(self, obj):
        try:
            return obj.partner['name']
        except KeyError:
            return 'N/A'


class AuditFilterForm(forms.Form):
    date_of_final_report = DateRangePickerField(
        label='Date of Final Report',
        required=False,
    )

class AuditViewSet(DataMartViewSet):
    querystringfilter_form_base_class = AuditFilterForm

    serializer_class = AuditSerializer
    queryset = models.Audit.objects.all()
    filter_fields = (
        'date_of_final_report',
    )

    def get_querystringfilter_form(self, request, filter):
        return AuditFilterForm(request.GET, filter.form_prefix)
