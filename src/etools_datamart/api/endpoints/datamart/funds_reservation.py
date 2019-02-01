from django import forms

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class FundsReservationSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FundsReservation
        exclude = None
        fields = '__all__'


class FundsReservationFilterForm(forms.Form):
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)
    submission_date = DateRangePickerField(label='Submitted between',
                                           required=False)

    # document_type__in = Select2MultipleChoiceField(label='Document Type',
    #                                                choices=PartnersIntervention.INTERVENTION_TYPES,
    #                                                required=False)


class FundsReservationViewSet(common.DataMartViewSet):
    serializer_class = FundsReservationSerializer
    queryset = models.FundsReservation.objects.all()
    filter_fields = ('vendor_code', 'fr_type', 'start_date')

    def get_querystringfilter_form(self, request, filter):
        return FundsReservationFilterForm(request.GET, filter.form_prefix)
