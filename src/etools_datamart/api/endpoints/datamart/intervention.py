# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import InterventionSerializerBudget, InterventionSerializerFull
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.models import PartnersIntervention

from .. import common
from . import serializers


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


class InterventionViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = InterventionFilterForm

    serializer_class = serializers.InterventionSerializer
    queryset = models.Intervention.objects.all()
    filter_fields = ('status', 'last_modify_date', 'document_type',
                     'start_date', 'submission_date',)
    serializers_fieldsets = {'std': None,
                             'full': InterventionSerializerFull,
                             'budget': InterventionSerializerBudget,
                             'short': ["title", "number", "country_name", "start_date"]}

    def get_querystringfilter_form(self, request, filter):
        return InterventionFilterForm(request.GET, filter.form_prefix)
