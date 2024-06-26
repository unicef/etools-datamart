from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2ChoiceField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import TravelType

from .. import common


class TripSerializer(DataMartSerializer):
    trip_url = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = models.Trip
        exclude = (
            "seen",
            "source_id",
        )

    def get_trip_url(self, obj):
        return "%s/%s?schema=%s" % (config.ETOOLS_ADDRESS, obj.trip_url, obj.schema_name)


class TripLightSerializer(DataMartSerializer):
    trip_url = serializers.SerializerMethodField()

    def get_trip_url(self, obj):
        return "%s/%s?schema=%s" % (config.ETOOLS_ADDRESS, obj.trip_url, obj.schema_name)

    class Meta:
        model = models.Trip
        fields = (
            "trip_url",
            "seen",
            "last_modify_date",
            "country_name",
            "additional_note",
            "created",
            "currency_code",
            "end_date",
            "international_travel",
            "locations",
            "mode_of_travel",
            "office_name",
            "partner_name",
            "pd_ssfa_reference_number",
            "pd_ssfa_title",
            "primary_traveler",
            "purpose",
            "reference_number",
            "report_note",
            "section_name",
            "start_date",
            "status",
            "supervisor_email",
            "ta_required",
            "traveler_email",
            "trip_attachments",
            "trip_activity_date",
            "trip_activity_type",
            "trip_activity_reference_number",
            "vendor_number",
            "source_activity_id",
        )


class TripFilterForm(forms.Form):
    # travel_reference_number__istartswith = forms.CharField(label='Reference Number',
    #                                                        required=False)
    travel_type = forms.CharField(label="Travel Type", required=False)
    trip_activity_type__in = Select2MultipleChoiceField(
        label="Activity Type", required=False, choices=TravelType.CHOICES
    )
    result_type = Select2MultipleChoiceField(
        label="Result Type",
        required=False,
        choices=(
            ("Activity", "Activity"),
            ("Outcome", "Outcome"),
            ("Output", "Output"),
        ),
    )
    mode_of_travel__acontains = Select2MultipleChoiceField(
        label="Mode Of Travel", required=False, choices=models.ModeOfTravel.CHOICES
    )
    # primary_traveler__istartswith = forms.CharField(label='Primary Traveler',
    #                                                 required=False)
    start_date = DateRangePickerField(label="Start Date between", required=False)

    end_date = DateRangePickerField(label="End Date between", required=False)
    international_travel = Select2ChoiceField(choices=(("", "All"), (1, "Yes"), (0, "No")), required=False)

    ta_required = Select2ChoiceField(choices=(("", "All"), (1, "Yes"), (0, "No")), required=False)

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if "mode_of_travel__acontains" in filters:
            filters.setlist("mode_of_travel__acontains", data["mode_of_travel__acontains"].split(","))
        if "trip_activity_type__in" in filters:
            filters.setlist("trip_activity_type__in", data["trip_activity_type__in"].split(","))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class TripViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = TripFilterForm

    serializer_class = TripSerializer
    serializers_fieldsets = {
        "light": TripLightSerializer,
    }
    queryset = models.Trip.objects.all()
    filter_fields = (
        "travel_type",
        "trip_activity_type",
        "result_type",
        # 'primary_traveler',
        "start_date",
        "end_date",
        "international_travel",
        "mode_of_travel",
        "ta_required",
    )
    ordering_fields = (
        "id",
        "created",
    )

    def get_querystringfilter_form(self, request, filter):
        return TripFilterForm(request.GET, filter.form_prefix)
