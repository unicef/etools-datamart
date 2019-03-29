from django import forms

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class ActionPointSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.ActionPoint
        exclude = None
        fields = '__all__'


class ActionPointFilterForm(forms.Form):
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)
    submission_date = DateRangePickerField(label='Submitted between',
                                           required=False)

    # document_type__in = Select2MultipleChoiceField(label='Document Type',
    #                                                choices=PartnersIntervention.INTERVENTION_TYPES,
    #                                                required=False)


class ActionPointViewSet(common.DataMartViewSet):
    serializer_class = ActionPointSerializer
    queryset = models.ActionPoint.objects.all()
    filter_fields = ('vendor_code', 'fr_type', 'start_date')
