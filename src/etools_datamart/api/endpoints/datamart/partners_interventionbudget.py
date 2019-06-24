from django import forms

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.datamart.intervention import InterventionSerializerV2
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.models import PartnersIntervention


class InterventionFilterForm(forms.Form):
    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=PartnersIntervention.STATUSES,
                                            required=False)
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)
    submission_date = DateRangePickerField(label='Submitted between',
                                           required=False)

    document_type__in = Select2MultipleChoiceField(label='Document Type',
                                                   choices=PartnersIntervention.INTERVENTION_TYPES,
                                                   required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class InterventionBudgetSerializerV2(InterventionSerializerV2):
    # vendor_number = serializers.CharField(source='vendor_number')
    # pd_ssfa_type = serializers.CharField(source='doocument_type')
    # pd_ssfa_reference_number = serializers.CharField(source='reference_number')
    # pd_ssfa_title = serializers.CharField(source='title')
    # pd_ssfa_status = serializers.CharField(source='status')
    # pd_ssfa_start_date = serializers.CharField(source='start_date')
    # pd_ssfa_end_date = serializers.CharField(source='end_date')
    # pd_ssfa_submission_date = serializers.CharField(source='submission_date')
    # pd_ssfa_submission_date_prc = serializers.CharField(source='submission_date_prc')

    class Meta:
        model = models.InterventionBudget
        fields = InterventionSerializerV2.Meta.fields + (
            'budget_cso_contribution',
            'budget_currency',
            'budget_total',
            'budget_unicef_cash',
            'budget_unicef_supply',
            'fr_numbers')


class InterventionBudgetSerializerFull(DataMartSerializer):
    class Meta:
        model = models.InterventionBudget
        exclude = ()


class InterventionBudgetSerializer(DataMartSerializer):
    class Meta:
        model = models.InterventionBudget
        fields = ('number', 'title', 'status', 'start_date', 'end_date',
                  'partner_contribution', 'unicef_cash', 'in_kind_amount',
                  'partner_contribution_local', 'unicef_cash_local', 'in_kind_amount_local',
                  'total', 'total_local', 'currency',
                  )


class InterventionBudgetSerializerPlain(InterventionBudgetSerializerV2):
    class Meta:
        model = models.InterventionBudget
        exclude = ('fr_numbers_data',
                   'cp_outputs_data',
                   'partner_focal_points_data',
                   'sections_data',
                   'unicef_focal_points_data',
                   )


class InterventionBudgetViewSet(common.DataMartViewSet):
    serializer_class = InterventionBudgetSerializer
    queryset = models.InterventionBudget.objects.all()
    serializers_fieldsets = {'std': None,
                             'plain': InterventionBudgetSerializerPlain,
                             'v2': InterventionBudgetSerializerV2,
                             'full': InterventionBudgetSerializerFull,
                             }
