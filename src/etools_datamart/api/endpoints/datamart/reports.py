from rest_framework import serializers

from etools_datamart.api.endpoints import common
from etools_datamart.apps.mart.data import models


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ('code', 'wbs', 'name', 'from_date', 'to_date')


class OutcomeViewSet(common.DataMartViewSet):
    serializer_class = OutcomeSerializer
    queryset = models.Result.objects.filter(result_type='Outcome')
    filter_fields = ('code', 'wbs')
    search_fields = ('name', )


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ('wbs', 'name', 'from_date', 'to_date', 'humanitarian_marker_code', 'humanitarian_marker_name',
                  'programme_area_code', 'programme_area_name')


class OutputViewSet(common.DataMartViewSet):
    serializer_class = OutputSerializer
    queryset = models.Result.objects.filter(result_type='Output')
    filter_fields = ('wbs', 'humanitarian_marker_code')
    search_fields = ('name', 'humanitarian_marker_name')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ('wbs', 'name', 'from_date', 'to_date', 'sic_code', 'sic_name', 'gic_code', 'gic_name',
                  'activity_focus_code', 'activity_focus_name', 'humanitarian_tag')


class ActivityViewSet(common.DataMartViewSet):
    serializer_class = ActivitySerializer
    queryset = models.Result.objects.filter(result_type='Activity')
    filter_fields = ('wbs', 'activity_focus_code', 'sic_code', 'gic_code')
    search_fields = ('name', 'activity_focus_name', 'humanitarian_tag', 'sic_name', 'gic_name')
