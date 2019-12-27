from django import forms

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.ordering import OrderingFilter

from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.filtering import DatamartQueryStringFilterBackend
from etools_datamart.apps.mart.prp import models


class DataReportFilterForm(forms.Form):
    pass


class DataReportSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.DataReport
        exclude = None
        fields = '__all__'


class DataReportViewSet(DataMartViewSet):
    serializer_class = DataReportSerializer
    queryset = models.DataReport.objects.all()
    # filter_fields = ('created', 'date_of_completion', 'due_date', 'high_priority')
    serializers_fieldsets = {'std': DataReportSerializer, }
    querystringfilter_form_base_class = DataReportFilterForm
    filter_backends = [DatamartQueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter,
                       ]

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
