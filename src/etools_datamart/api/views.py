from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from etools_datamart.apps.etools import models
from . import serializers


class ApiMixin:
    permission_classes = []


class ReadOnlyModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination  # PageNumberPagination


class ModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pass


class PartnerViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.PartnerSerializer
    queryset = models.PartnersPartnerorganization.objects.all()


class ReportsResultViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ReportsResultSerializer
    queryset = models.ReportsResult.objects.select_related('result_type')
