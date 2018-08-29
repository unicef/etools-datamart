from etools_datamart.apps.etools import models

from . import common
from .. import serializers


class ReportsResultViewSet(common.MultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related('result_type')


class ReportsResultTypeViewSet(common.MultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related('result_type')


class AppliedindicatorViewSet(common.MultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.AppliedindicatorSerializer
    queryset = models.ReportsAppliedindicator.objects.all()
