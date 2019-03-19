# -*- coding: utf-8 -*-
# import django_filters
from django import forms
from django.forms import CharField

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class TravelActivitySerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.TravelActivity
        exclude = ('seen', 'source_id', 'location_source_id')


class TravelActivityFilterForm(forms.Form):
    travel_reference_number__istartswith = CharField(label='Reference Number')
    travel_type = CharField(label='Travel Type')
    primary_traveler__istartswith = CharField(label='Primary Traveler')
    start_date = DateRangePickerField(label='Started between',
                                      required=False)

    end_date = DateRangePickerField(label='Ended between',
                                    required=False)


class TravelActivityViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = TravelActivityFilterForm

    serializer_class = TravelActivitySerializer
    queryset = models.TravelActivity.objects.all()
    filter_fields = ('travel_reference_number', 'travel_type', 'primary_traveler')
    ordering_fields = ("id", "created",)
