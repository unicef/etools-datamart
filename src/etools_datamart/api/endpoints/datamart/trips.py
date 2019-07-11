# -*- coding: utf-8 -*-
# import django_filters
from constance import config
from django import forms
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class TripSerializer(DataMartSerializer):
    trip_url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.Trip
        exclude = ('seen', 'source_id',)

    def get_trip_url(self, obj):
        return "%s/%s?schema=%s" % (config.ETOOLS_ADDRESS,
                                    obj.trip_url,
                                    obj.schema_name)


class TripFilterForm(forms.Form):
    travel_reference_number__istartswith = forms.CharField(label='Reference Number',
                                                           required=False)
    travel_type = forms.CharField(label='Travel Type',
                                  required=False)
    result_type = Select2MultipleChoiceField(label='Result Type',
                                             required=False,
                                             choices=(('Activity', 'Activity'),
                                                      ('Outcome', 'Outcome'),
                                                      ('Output', 'Output'),
                                                      ))
    primary_traveler__istartswith = forms.CharField(label='Primary Traveler',
                                                    required=False)
    date = DateRangePickerField(label='Date between',
                                required=False)


class TripViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = TripFilterForm

    serializer_class = TripSerializer
    queryset = models.Trip.objects.all()
    filter_fields = ('is_second_traveler',
                     'mode_of_travel',
                     'start_date',
                     'status')
    ordering_fields = ("id", "created",)

    def get_querystringfilter_form(self, request, filter):
        return TripFilterForm(request.GET, filter.form_prefix)
