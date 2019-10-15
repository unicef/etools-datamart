from django import forms

from unicef_rest_framework.forms import CleareableSelect2ChoiceField, DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.endpoints.rapidpro._base_ import RapidProViewSet
from etools_datamart.apps.rapidpro import models


class FlowStartFilterForm(forms.Form):
    archived = CleareableSelect2ChoiceField(required=False,
                                            choices=((None, 'All'),
                                                     (False, 'False'),
                                                     (True, 'True'),))

    created_on = DateRangePickerField(label='Created between',
                                            required=False)


class FlowStartSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FlowStart
        exclude = ()


class FlowStartViewSet(RapidProViewSet):
    serializer_class = FlowStartSerializer
    queryset = models.FlowStart.objects.all()
    # filter_fields = ('created', 'date_of_completion', 'due_date')
    serializers_fieldsets = {'std': FlowStartSerializer}
    querystringfilter_form_base_class = FlowStartFilterForm
    filter_fields = ['organization', ]

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_querystringfilter_form(self, request, filter):
        return FlowStartFilterForm(request.GET, filter.form_prefix)
