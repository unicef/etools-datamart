# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.enrichment.consts import PartnersAgreementConst

from .. import common


class PartnerAgreementSerializer(DataMartSerializer):
    agreement_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Agreement
        fields = ('agreement_type',
                  'reference_number',
                  'status',
                  'start',
                  'end',
                  'partner_name',
                  'vendor_number',
                  'country_name',
                  'schema_name',
                  'country_programme',
                  'signed_by_partner',
                  'signed_by_partner_date',
                  'signed_by_unicef_date',
                  'partner_authorized_officers',
                  'special_conditions_pca',
                  'agreement_amendments',
                  'agreement_url',
                  )

    def get_agreement_url(self, obj):
        return '%s/pmp/agreements/%d/details?schema=%s' % (config.ETOOLS_ADDRESS,
                                                           obj.source_id,
                                                           obj.schema_name)


class AgreementFilterForm(forms.Form):
    agreement_type__in = Select2MultipleChoiceField(label='Agreement Type',
                                                    choices=PartnersAgreementConst.AGREEMENT_TYPES,
                                                    required=False)
    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=PartnersAgreementConst.STATUS_CHOICES,
                                            required=False)
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        initial = {"hidden": ""}
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        if 'agreement_type__in' in filters:
            filters.setlist('agreement_type__in', data['agreement_type__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class PartnerAgreementViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = AgreementFilterForm

    serializer_class = PartnerAgreementSerializer
    queryset = models.Agreement.objects.all()
    filter_fields = ('agreement_type', 'status', 'last_modify_date')

    def get_querystringfilter_form(self, request, filter):
        return AgreementFilterForm(request.GET, filter.form_prefix)
