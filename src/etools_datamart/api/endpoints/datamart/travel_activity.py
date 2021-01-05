from django import forms

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class TravelActivitySerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.TravelActivity
        exclude = ('seen', 'source_id', 'location_source_id')


class TravelActivityFilterForm(forms.Form):
    travel_reference_number__istartswith = forms.CharField(label='Reference Number',
                                                           required=False)
    travel_type = forms.CharField(label='Travel Type',
                                  required=False)
    result_type = Select2MultipleChoiceField(label='Result Type',
                                             required=False,
                                             choices=(('Activity', 'Activity'),
                                                      ('Outcome', 'Outcome'),
                                                      ('Output', 'Output'),
                                                      ))
    primary_traveler__istartswith = forms.CharField(label='Primary Traveler',
                                                    required=False)
    date = DateRangePickerField(label='Date between',
                                      required=False)


class TravelActivityViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = TravelActivityFilterForm

    serializer_class = TravelActivitySerializer
    queryset = models.TravelActivity.objects.all()
    filter_fields = ('travel_reference_number', 'travel_type', 'primary_traveler',
                     'result_type', 'date')
    ordering_fields = ("id", "created",)

    def get_querystringfilter_form(self, request, filter):
        return TravelActivityFilterForm(request.GET, filter.form_prefix)
