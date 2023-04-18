from django import forms

from unicef_rest_framework.forms import CleareableSelect2ChoiceField, DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.endpoints.rapidpro._base_ import RapidProViewSet
from etools_datamart.apps.mart.rapidpro import models


class CampaignFilterForm(forms.Form):
    archived = CleareableSelect2ChoiceField(
        required=False,
        choices=(
            (None, "All"),
            (False, "False"),
            (True, "True"),
        ),
    )

    created_on = DateRangePickerField(label="Created between", required=False)


class CampaignSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Campaign
        exclude = ()


class CampaignViewSet(RapidProViewSet):
    serializer_class = CampaignSerializer
    queryset = models.Campaign.objects.all()
    serializers_fieldsets = {"std": CampaignSerializer}
    querystringfilter_form_base_class = CampaignFilterForm
    filter_fields = ["organization", "archived", "created_on"]

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_querystringfilter_form(self, request, filter):
        return CampaignFilterForm(request.GET, filter.form_prefix)
