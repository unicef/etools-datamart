from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.sources.etools import models


class ReportsResultViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related("result_type")


class ReportsResultTypeViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related("result_type")


class AppliedindicatorViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.AppliedindicatorSerializer
    queryset = models.ReportsAppliedindicator.objects.all()
