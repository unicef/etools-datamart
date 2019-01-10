# -*- coding: utf-8 -*-
# import django_filters
from collections import OrderedDict

from django import forms

from unicef_rest_framework.forms import DatePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import InterventionSerializerFull
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.models import PartnersIntervention

from . import serializers
from .. import common


class InterventionFilterForm(forms.Form):
    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=PartnersIntervention.STATUSES,
                                            required=False)
    last_modify_date__gte = DatePickerField(label='Modified after',
                                            required=False)

    start_date__gte = DatePickerField(label='Started after',
                                      required=False)

    submission_date__gt = DatePickerField(label='Submitted after',
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
                             'short': ["title", "number", "country_name", "start_date"]}

    def get_schema_fields(self):
        return super().get_schema_fields()

    def get_querystringfilter_form(self, request, filter):
        fields = OrderedDict([
            (name, forms.CharField(required=False))
            for name in self.filter_fields if name not in ('status',
                                                           'start_date',
                                                           'submission_date',
                                                           'document_type',
                                                           'last_modify_date')])

        return type(str('%sForm' % self.__class__.__name__),
                    (InterventionFilterForm,), fields)(request.GET, filter.form_prefix)
