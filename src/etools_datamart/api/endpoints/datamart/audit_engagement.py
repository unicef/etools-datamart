# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class EngagementSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Engagement
        exclude = ('seen', 'source_id',)


class EngagementFilterForm(forms.Form):
    engagement_type__in = Select2MultipleChoiceField(label='Engagement Type',
                                                     choices=models.Engagement.TYPES,
                                                     required=False)
    partner_contacted_at = DateRangePickerField(label='Date IP was contacted',
                                                required=False)

    start_date = DateRangePickerField(label='Period Start Date',
                                      required=False)

    end_date = DateRangePickerField(label='Period End Date',
                                    required=False)


class EngagementViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = EngagementFilterForm

    serializer_class = EngagementSerializer
    queryset = models.Engagement.objects.all()
    filter_fields = ('engagement_type', 'partner_contacted_at',
                     'start_date', 'end_date')

    def get_querystringfilter_form(self, request, filter):
        return EngagementFilterForm(request.GET, filter.form_prefix)
