# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DatePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import PartnerOrganizationConst, PartnersInterventionConst

from .. import common


class PMPIndicatorsSerializer(DataMartSerializer):
    partner_link = serializers.SerializerMethodField()
    intervention_link = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.PMPIndicators

    def get_partner_link(self, obj):
        return "%s/pmp/partners/%s/details/?schema=%s" % (config.ETOOLS_ADDRESS,
                                                          obj.partner_id,
                                                          obj.schema_name)

    def get_intervention_link(self, obj):
        return "%s/pmp/interventions/%s/details/?schema=%s" % (config.ETOOLS_ADDRESS,
                                                               obj.intervention_id,
                                                               obj.schema_name)


class PMPIndicatorFilterForm(forms.Form):
    partner_type__in = Select2MultipleChoiceField(label='Partner Type',
                                                  choices=PartnerOrganizationConst.CSO_TYPES,
                                                  required=False)

    pd_ssfa_status__in = Select2MultipleChoiceField(label='Status',
                                                    choices=PartnersInterventionConst.STATUSES,
                                                    required=False)

    last_modify_date__gte = DatePickerField(label='Modified after',
                                            required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'partner_type__in' in filters:
            filters.setlist('partner_type__in', data['partner_type__in'].split(','))
        if 'pd_ssfa_status__in' in filters:
            filters.setlist('pd_ssfa_status__in', data['pd_ssfa_status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class PMPIndicatorsViewSet(common.DataMartViewSet):
    serializer_class = PMPIndicatorsSerializer
    queryset = models.PMPIndicators.objects.all()
    filter_fields = ('partner_type', 'last_modify_date', 'pd_ssfa_status')
    serializers_fieldsets = {"std": None,
                             "brief": ["id", "country_name",
                                       "partner_name", "partner_type", "total_budget",
                                       "unicef_budget", "currency",
                                       ],
                             "ssfa": ["pd_ssfa_ref",
                                      "pd_ssfa_status",
                                      "pd_ssfa_start_date",
                                      "pd_ssfa_creation_date",
                                      "pd_ssfa_end_date"]}

    def get_querystringfilter_form(self, request, filter):
        fields = OrderedDict([
            (name, forms.CharField(required=False))
            for name in self.filter_fields if name not in ('partner_type',
                                                           'pd_ssfa_status',
                                                           'last_modify_date')])

        return type(str('%sForm' % self.__class__.__name__),
                    (PMPIndicatorFilterForm,), fields)(request.GET, filter.form_prefix)
