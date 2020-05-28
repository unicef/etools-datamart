from django import forms

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.ordering import OrderingFilter

from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.filtering import DatamartQueryStringFilterBackend
from etools_datamart.apps.mart.prp import models
from unicef_rest_framework.forms import Select2MultipleChoiceField


class DataReportFilterForm(forms.Form):
    country_name__in = Select2MultipleChoiceField(
        label='Country',
        choices=[],
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country_name__in"].choices = [
            (c.country_name, c.country_name)
            for c in models.DataReport.objects.distinct(
                    "country_name"
            ).order_by("country_name")
        ]


class DataReportSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.DataReport
        exclude = None
        fields = '__all__'


class DataReportViewSet(DataMartViewSet):
    serializer_class = DataReportSerializer
    queryset = models.DataReport.objects.all()
    filter_fields = ('country_name',)
    serializers_fieldsets = {'std': DataReportSerializer, }
    querystringfilter_form_base_class = DataReportFilterForm
    filter_backends = [
        DatamartQueryStringFilterBackend,
        OrderingFilter,
        DynamicSerializerFilter,
    ]

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
