from django import forms

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.datamart.intervention import (InterventionSerializer, InterventionSerializerFull,
                                                                 InterventionSerializerPlain, InterventionSerializerV2,)
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst


class InterventionFilterForm(forms.Form):
    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=PartnersInterventionConst.STATUSES,
                                            required=False)
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)
    submission_date = DateRangePickerField(label='Submitted between',
                                           required=False)

    document_type__in = Select2MultipleChoiceField(label='Document Type',
                                                   choices=PartnersInterventionConst.INTERVENTION_TYPES,
                                                   required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class InterventionBudgetSerializer(InterventionSerializer):
    class Meta:
        model = models.InterventionBudget
        exclude = InterventionSerializer.Meta.exclude


class InterventionBudgetSerializerV2(InterventionSerializerV2):
    class Meta:
        model = models.InterventionBudget
        fields = InterventionSerializerV2.Meta.fields + (
            'budget_cso_contribution',
            'budget_currency',
            'budget_total',
            'budget_unicef_cash',
            'budget_unicef_supply',
            'fr_numbers')


class InterventionBudgetSerializerFull(InterventionSerializerFull):
    class Meta:
        model = models.InterventionBudget
        exclude = InterventionSerializerFull.Meta.exclude


class InterventionBudgetSerializerPlain(InterventionSerializerPlain):
    class Meta:
        model = models.InterventionBudget
        exclude = InterventionSerializerPlain.Meta.exclude


class InterventionBudgetViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = InterventionFilterForm
    filter_fields = ('document_type', 'last_modify_date', 'start_date', 'status', 'submission_date')
    serializer_class = InterventionBudgetSerializer
    queryset = models.InterventionBudget.objects.all()
    serializers_fieldsets = {'std': None,
                             'plain': InterventionBudgetSerializerPlain,
                             'v2': InterventionBudgetSerializerV2,
                             'full': InterventionBudgetSerializerFull,
                             }
