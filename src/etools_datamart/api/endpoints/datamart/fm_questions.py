from datetime import datetime

from django import forms
from constance import config

from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from unicef_rest_framework.forms import Select2ChoiceField


class FMQuestionSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMQuestion


class FMQuestionFilterForm(forms.Form):
    year = Select2ChoiceField(
        label="Monitoring Activity End Year",
        choices=[(r, r) for r in range(datetime.now().year, config.START_YEAR_FILTER - 1, -1)],
        required=False,
    )


class FMQuestionViewSet(DataMartViewSet):
    serializer_class = FMQuestionSerializer
    queryset = models.FMQuestion.objects.all()
    filter_fields = ("year",)
    querystringfilter_form_base_class = FMQuestionFilterForm

    def drfqs_filter_year(self, filters, exclude, value, **payload):
        filters["monitoring_activity_end_date__contains"] = value
        return filters, exclude


class FMOntrackSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMOntrack


class FMOntrackViewSet(DataMartViewSet):
    serializer_class = FMOntrackSerializer
    queryset = models.FMOntrack.objects.all()


class FMOptionsSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMOptions


class FMOptionsViewSet(DataMartViewSet):
    serializer_class = FMOptionsSerializer
    queryset = models.FMOptions.objects.all()
