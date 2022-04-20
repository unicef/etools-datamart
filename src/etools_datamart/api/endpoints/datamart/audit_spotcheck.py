from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from ..common import DataMartViewSet


class SpotCheckFindingSerializer(DataMartSerializer):
    partner_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.SpotCheckFindings
        exclude = ('seen', 'source_id',)

    def get_url(self, obj):
        try:
            return "{}/ap/spot-checks/{}/overview".format(
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


class SpotCheckFindingDataSerializer(SpotCheckFindingSerializer):
    pass


class SpotCheckFindingFilterForm(forms.Form):
    date_of_final_report = DateRangePickerField(
        label='Date of Final Report',
        required=False,
    )


class SpotCheckFindingViewSet(DataMartViewSet):
    querystringfilter_form_base_class = SpotCheckFindingFilterForm

    serializer_class = SpotCheckFindingSerializer
    queryset = models.SpotCheckFindings.objects.all()
    filter_fields = (
        'date_of_final_report',
    )
    serializers_fieldsets = {
        'std': SpotCheckFindingSerializer,
        'dates': SpotCheckFindingDataSerializer
    }

    def get_querystringfilter_form(self, request, filter):
        return SpotCheckFindingFilterForm(request.GET, filter.form_prefix)
