from django import forms

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class FundsReservationSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FundsReservation
        exclude = None
        fields = "__all__"


class FundsReservationFilterForm(forms.Form):
    last_modify_date = DateRangePickerField(label="Modified between", required=False)

    start_date = DateRangePickerField(label="Started between", required=False)
    submission_date = DateRangePickerField(label="Submitted between", required=False)

    # document_type__in = Select2MultipleChoiceField(label='Document Type',
    #                                                choices=PartnersIntervention.INTERVENTION_TYPES,
    #                                                required=False)


class FundsReservationLightSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FundsReservation
        fields = [
            "country_name",
            "pd_reference_number",
            "vendor_code",
            "fr_number",
            "fr_ref_number",
            "wbs",
            "overall_amount_dc",
            "actual_amt",
            "actual_amt_local",
            "total_amt_local",
        ]
        exclude = None


class FundsReservationViewSet(common.DataMartViewSet):
    serializer_class = FundsReservationSerializer
    queryset = models.FundsReservation.objects.all()
    filter_fields = ("vendor_code", "fr_type", "start_date", "last_modify_date", "submission_date")
    search_fields = ("vendor_code", "fr_number")

    serializers_fieldsets = {"std": None, "light": FundsReservationLightSerializer}

    def get_querystringfilter_form(self, request, filter):
        return FundsReservationFilterForm(request.GET, filter.form_prefix)
