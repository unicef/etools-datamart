# -*- coding: utf-8 -*-
from month_field.rest_framework import MonthFilterBackend

from etools_datamart.apps.data import models

from .. import common
from . import serializers


class UserStatsViewSet(common.DataMartViewSet):
    serializer_class = serializers.UserStatsSerializer
    filter_backends = [MonthFilterBackend] + common.DataMartViewSet.filter_backends
    queryset = models.UserStats.objects.all()
    filter_fields = ('last_modify_date', )
    serializers_fieldsets = {"std": None}
