# -*- coding: utf-8 -*-
from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2ChoiceField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.enrichment.consts import TpmTpmvisitConst

from .. import common


class TPMActivityFilterForm(forms.Form):
    # is_pv = forms.BooleanField(required=False)
    is_pv = Select2ChoiceField(choices=(("-", 'All'),
                                        (1, 'True'),
                                        (0, 'False')), required=False)
    visit_status__in = Select2MultipleChoiceField(label='Status',
                                                  choices=TpmTpmvisitConst.STATUSES,
                                                  required=False)
    date = DateRangePickerField(label='Date',
                                required=False)

    visit_start_date = DateRangePickerField(label='Visit Start Date',
                                            required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'visit_status__in' in filters:
            filters.setlist('visit_status__in', data['visit_status__in'].split(','))
        # if 'is_pv' in filters:
        #     filters.setlist('is_pv', 1)
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class TPMActivitySerializer(DataMartSerializer):
    visit_url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.TPMActivity

    def get_visit_url(self, obj):
        return "%s/%s?schema=%s" % (config.ETOOLS_ADDRESS,
                                    obj.visit_url,
                                    obj.schema_name)


class TPMActivityViewSet(common.DataMartViewSet):
    serializer_class = TPMActivitySerializer
    queryset = models.TPMActivity.objects.all()
    filter_fields = ('date', 'is_pv', 'visit_status')
    ordering_fields = ("id", "created",)
    querystringfilter_form_base_class = TPMActivityFilterForm

    def get_querystringfilter_form(self, request, filter):
        return TPMActivityFilterForm(request.GET, filter.form_prefix)

    def drfqs_filter_is_pv(self, filters, exclude, value, **payload):
        if value == '1':
            filters['is_pv'] = True
        elif value == '0':
            filters['is_pv'] = False

        return filters, exclude
