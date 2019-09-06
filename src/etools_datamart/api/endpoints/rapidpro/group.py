from django import forms

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.endpoints.rapidpro._base_ import RapidProViewSet
from etools_datamart.apps.rapidpro import models


class GroupSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Group
        exclude = ()


class GroupFilterForm(forms.Form):
    organization = DateRangePickerField(label='Created between', required=False)


class GroupViewSet(RapidProViewSet):
    serializer_class = GroupSerializer
    queryset = models.Group.objects.all()
    # filter_fields = ('created', 'date_of_completion', 'due_date')
    serializers_fieldsets = {'std': GroupSerializer}
    querystringfilter_form_base_class = GroupFilterForm

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
