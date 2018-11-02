# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class UserStatsViewSet(common.APIReadOnlyModelViewSet):
    serializer_class = serializers.UserStatsSerializer
    queryset = models.UserStats.objects.all()
    filter_fields = ('country_name', 'month')

    def drf_ignore_filter(self, request, field):
        return super().drf_ignore_filter(request, field)
