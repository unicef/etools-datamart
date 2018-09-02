from etools_datamart.apps.etools import models

from . import common
from .. import serializers


class ReportsResultViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related('result_type')


class ReportsResultTypeViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related('result_type')


class AppliedindicatorViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.AppliedindicatorSerializer
    queryset = models.ReportsAppliedindicator.objects.all()
