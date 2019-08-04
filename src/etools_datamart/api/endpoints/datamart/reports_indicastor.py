# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class IndicatorSerializer(DataMartSerializer):
    # last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    class Meta(DataMartSerializer.Meta):
        model = models.ReportIndicator
        exclude = None
        fields = (
            "pd_sffa_reference_number",
            # "cp_output",
            # "cp_output_id",
            # "pd_output_name",
            # "pd_output_section",
            # "pd_output_indicator_title",
            "cluster_indicator_id",
            "cluster_indicator_title",
            "cluster_name",
            "response_plan_name",
            "is_active",
            "is_high_frequency",
            "means_of_verification",
            "measurement_specifications",
            "country_name",
            "schema_name",
            "area_code",
            # "location_name",
            # "location_pcode",
            # "location_level",
            # "location_levelname",
            "unit",
            "label",
            "denominator_label",
            "baseline_denominator",
            "target_denominator",
            "numerator_label",
            "baseline_numerator",
            "target_numerator",
            # "disaggregation_name",
            # "disaggregation_active",
            # "source_disaggregation_id",
            # "pd_output_indicator",
            "last_modify_date")


class IndicatorViewSet(common.DataMartViewSet):
    serializer_class = IndicatorSerializer
    queryset = models.ReportIndicator.objects.all()
    filter_fields = ('year', 'last_modify_date')
