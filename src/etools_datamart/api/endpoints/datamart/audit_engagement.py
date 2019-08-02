# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from ..common import DataMartViewSet


class EngagementSerializerSimple(DataMartSerializer):
    partner = serializers.IntegerField(source='partner.id')
    schema = serializers.CharField(source='schema_name')

    class Meta(DataMartSerializer.Meta):
        model = models.Engagement
        exclude = None
        fields = ('country_name',
                  'schema',
                  'created',
                  'modified',
                  'status',
                  'partner_contacted_at',
                  'engagement_type',
                  'start_date',
                  'end_date',
                  'total_value',
                  'date_of_field_visit',
                  'date_of_draft_report_to_ip',
                  'date_of_comments_by_ip',
                  'date_of_draft_report_to_unicef',
                  'date_of_comments_by_unicef',
                  'date_of_report_submit',
                  'date_of_final_report',
                  'date_of_cancel',
                  'amount_refunded',
                  'additional_supporting_documentation_provided',
                  'justification_provided_and_accepted',
                  'write_off_required',
                  'cancel_comment',
                  'explanation_for_additional_information',
                  'joint_audit',
                  'shared_ip_with',
                  'exchange_rate',
                  'partner',
                  'agreement',
                  'po_item',
                  )


class EngagementSerializer(DataMartSerializer):
    partner_name = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.Engagement
        exclude = ('seen', 'source_id',)

    def get_partner_name(self, obj):
        try:
            return obj.partner['name']
        except KeyError:
            return 'N/A'


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


class EngagementViewSet(DataMartViewSet):
    querystringfilter_form_base_class = EngagementFilterForm

    serializer_class = EngagementSerializer
    queryset = models.Engagement.objects.all()
    filter_fields = ('engagement_type', 'partner_contacted_at',
                     'start_date', 'end_date')
    serializers_fieldsets = {'std': None,
                             'simple': EngagementSerializerSimple}

    def get_querystringfilter_form(self, request, filter):
        return EngagementFilterForm(request.GET, filter.form_prefix)
