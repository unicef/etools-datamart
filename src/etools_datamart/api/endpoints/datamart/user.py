# -*- coding: utf-8 -*-
from rest_framework.filters import OrderingFilter

from etools_datamart.api.filtering import MonthFilterBackend, SchemaFilterBackend
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class UserStatsViewSet(common.APIReadOnlyModelViewSet):
    serializer_class = serializers.UserStatsSerializer
    queryset = models.UserStats.objects.all()
    filter_backends = [MonthFilterBackend, SchemaFilterBackend, OrderingFilter]
    # filter_fields = ('country_name', )

    def drf_ignore_filter(self, request, field):
        return super().drf_ignore_filter(request, field)
