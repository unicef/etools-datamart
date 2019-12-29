# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts

from ..common import DataMartViewSet


class SpotCheckSerializerSimple(DataMartSerializer):
    partner = serializers.IntegerField(source='partner.id')
    schema = serializers.CharField(source='schema_name')

    class Meta(DataMartSerializer.Meta):
        model = models.SpotCheck
        exclude = None
        fields = ('country_name',
                  'schema',
                  'created',
                  'modified',
                  'reference_number',
                  'status',
                  'finding_id',
                  'category_of_observation',
                  'deadline_of_action',
                  'finding_priority',
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

#
# URL_MAP = {models.Engagement.TYPE_AUDIT: 'audit',
#            models.Engagement.TYPE_MICRO_ASSESSMENT: 'micro-assessments',
#            models.Engagement.TYPE_SPOT_CHECK: 'spot-checks',
#            models.Engagement.TYPE_SPECIAL_AUDIT: 'special-audits'
#            }


class SpotCheckSerializer(DataMartSerializer):
    partner_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.SpotCheck
        exclude = ('seen', 'source_id',)

    def get_url(self, obj):
        try:
            return "%s/ap/spot-checks/%s/overview" % (config.ETOOLS_ADDRESS, obj.source_id)
        except KeyError:
            return ""

    def get_partner_name(self, obj):
        try:
            return obj.partner['name']
        except KeyError:
            return 'N/A'


class SpotCheckFilterForm(forms.Form):
    partner_contacted_at = DateRangePickerField(label='Date IP was contacted',
                                                required=False)

    start_date = DateRangePickerField(label='Start Date',
                                      required=False)

    end_date = DateRangePickerField(label='End Date',
                                    required=False)

    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=AuditEngagementConsts.DISPLAY_STATUSES,
                                            required=False)

    audit_opinion__in = Select2MultipleChoiceField(label='Audit Opinion',
                                                   choices=models.Engagement.AUDIT_OPTIONS,
                                                   required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        if 'audit_opinion__in' in filters:
            filters.setlist('audit_opinion__in', data['audit_opinion__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class SpotCheckViewSet(DataMartViewSet):
    querystringfilter_form_base_class = SpotCheckFilterForm

    serializer_class = SpotCheckSerializer
    queryset = models.SpotCheck.objects.all()
    filter_fields = ('partner_contacted_at',
                     'start_date', 'end_date', 'status', 'audit_opinion')
    serializers_fieldsets = {'std': None,
                             'simple': SpotCheckSerializerSimple}

    def get_querystringfilter_form(self, request, filter):
        return SpotCheckFilterForm(request.GET, filter.form_prefix)
