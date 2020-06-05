from django import forms

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.forms import Select2MultipleChoiceField
from unicef_rest_framework.ordering import OrderingFilter

from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.filtering import DatamartQueryStringFilterBackend
from etools_datamart.apps.mart.prp import models
from etools_datamart.apps.sources.source_prp.enrichment.consts import PROGRESS_REPORT_STATUS, REPORTING_TYPES


class DataReportFilterForm(forms.Form):
    country_name__in = Select2MultipleChoiceField(
        label='Country',
        choices=[],
        required=False,
    )
    report_status__in = Select2MultipleChoiceField(
        label='Report Status',
        choices=PROGRESS_REPORT_STATUS,
        required=False,
    )
    report_type__in = Select2MultipleChoiceField(
        label='Type of Report',
        choices=REPORTING_TYPES,
        required=False,
    )
    section__icontains = Select2MultipleChoiceField(
        label='Section',
        choices=[],
        required=False,
    )

    def get_section_choices(self):
        sections = []
        for record in models.DataReport.objects.all():
            sections += [s.strip() for s in record.section.split(",")]
        return [(s, s) for s in set(sections)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["country_name__in"].choices = [
                (c.country_name, c.country_name)
                for c in models.DataReport.objects.distinct(
                        "country_name"
                ).order_by("country_name")
            ]
            self.fields["section__in"].choices = self.get_section_choices()
        except:
            # Ignore this exception, as it is used to catch exception during
            # changes to the DataReport model, or running migrations
            # Worse case is choice for filtering is blank
            pass


class DataReportSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.DataReport
        exclude = None
        fields = '__all__'


class DataReportViewSet(DataMartViewSet):
    serializer_class = DataReportSerializer
    queryset = models.DataReport.objects.all()
    filter_fields = ('country_name', 'report_status', 'report_type', 'section')
    serializers_fieldsets = {'std': DataReportSerializer, }
    querystringfilter_form_base_class = DataReportFilterForm
    filter_backends = [
        DatamartQueryStringFilterBackend,
        OrderingFilter,
        DynamicSerializerFilter,
    ]

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
