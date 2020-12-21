from django import forms

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class GrantSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Grant
        exclude = ('seen', 'source_id',)


class GrantFilterForm(forms.Form):
    expiry = DateRangePickerField(label='Date between',
                                  required=False)


class GrantViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = GrantFilterForm

    serializer_class = GrantSerializer
    queryset = models.Grant.objects.all()
    filter_fields = ('expiry',)
    ordering_fields = ("id", "name",)

    def get_querystringfilter_form(self, request, filter):
        return GrantFilterForm(request.GET, filter.form_prefix)
