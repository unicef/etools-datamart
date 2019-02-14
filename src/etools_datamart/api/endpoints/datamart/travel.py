# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.patch import T2FTravel_CHOICES

from .. import common


class TravelSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Travel


class TravelFilterForm(forms.Form):
    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=T2FTravel_CHOICES,
                                            required=False)
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)

    end_date = DateRangePickerField(label='Ended between',
                                    required=False)

    created = DateRangePickerField(label='Created between',
                                   required=False)

    approved_at = DateRangePickerField(label='Approved between',
                                       required=False)

    completed_at = DateRangePickerField(label='Completed between',
                                        required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class TravelViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = TravelFilterForm

    serializer_class = TravelSerializer
    queryset = models.Travel.objects.all()
    filter_fields = ('status', 'created'

                               'completed_at', 'approved_at', 'end_date', 'start_date')

    def get_querystringfilter_form(self, request, filter):
        return TravelFilterForm(request.GET, filter.form_prefix)
