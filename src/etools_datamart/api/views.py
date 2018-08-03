from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import CursorPagination

from etools_datamart.apps.etools import models
from . import serializers


class ApiMixin:
    permission_classes = []


def paginator(ordering='-created'):
    return type("TenantPaginator", (CursorPagination,), {'ordering': ordering})


class ReadOnlyModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pagination_class = paginator()
    filter_backends = [QueryStringFilterBackend]
    filter_blacklist = []
    filter_fields = []


class PartnerViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.PartnerSerializer
    queryset = models.PartnersPartnerorganization.objects.all()


class ReportsResultViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related('result_type')
