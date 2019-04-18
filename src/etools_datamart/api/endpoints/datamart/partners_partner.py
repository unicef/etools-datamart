# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from unicef_rest_framework.forms import CleareableSelect2ChoiceField, DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.enrichment.consts import PartnerType

from .. import common


class PartnerSerializerFull(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Partner


class PartnerSerializerStd(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Partner
        exclude = ('')


class PartnerSerializerShort(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Partner
        fields = ('name', 'alternate_name', 'partner_type', 'country', 'email')


class PartnerFilterForm(forms.Form):
    partner_type__in = Select2MultipleChoiceField(label='Partner Type',
                                                  choices=PartnerType.CHOICES,
                                                  required=False)
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)
    hidden = CleareableSelect2ChoiceField(required=False,
                                          choices=((None, 'All'),
                                                   (False, 'False'),
                                                   (True, 'True'),))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        initial = {"hidden": ""}
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class PartnerViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = PartnerFilterForm

    serializer_class = PartnerSerializerFull
    serializers_fieldsets = {'std': PartnerSerializerStd,
                             'full': PartnerSerializerFull,
                             'short': ["title", "number", "country_name", "start_date"]}
    queryset = models.Partner.objects.all()
    filter_fields = ('partner_type', 'hidden', 'cso_type', 'rating')
    ordering_fields = ("id", "name")

    def get_querystringfilter_form(self, request, filter):
        return PartnerFilterForm(request.GET, filter.form_prefix)
