# -*- coding: utf-8 -*-
# import django_filters
from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2ChoiceField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.data.models.trip import ModeOfTravel

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
    # travel_reference_number__istartswith = forms.CharField(label='Reference Number',
    #                                                        required=False)
    travel_type = forms.CharField(label='Travel Type',
                                  required=False)
    result_type = Select2MultipleChoiceField(label='Result Type',
                                             required=False,
                                             choices=(('Activity', 'Activity'),
                                                      ('Outcome', 'Outcome'),
                                                      ('Output', 'Output'),
                                                      ))
    mode_of_travel__acontains = Select2MultipleChoiceField(label='Mode Of Travel',
                                                           required=False,
                                                           choices=ModeOfTravel.CHOICES
                                                           )
    # primary_traveler__istartswith = forms.CharField(label='Primary Traveler',
    #                                                 required=False)
    start_date = DateRangePickerField(label='Start Date between',
                                      required=False)

    end_date = DateRangePickerField(label='End Date between',
                                    required=False)
    international_travel = Select2ChoiceField(choices=(("", 'All'),
                                                       (1, 'Yes'),
                                                       (0, 'No')), required=False)

    ta_required = Select2ChoiceField(choices=(("", 'All'),
                                              (1, 'Yes'),
                                              (0, 'No')), required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'mode_of_travel__acontains' in filters:
            filters.setlist('mode_of_travel__acontains', data['mode_of_travel__acontains'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class TripViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = TripFilterForm

    serializer_class = TripSerializer
    queryset = models.Trip.objects.all()
    filter_fields = ('travel_type',
                     'result_type',
                     # 'primary_traveler',
                     'start_date',
                     'end_date',
                     'international_travel',
                     'mode_of_travel',
                     'ta_required')
    ordering_fields = ("id", "created",)

    def get_querystringfilter_form(self, request, filter):
        return TripFilterForm(request.GET, filter.form_prefix)
