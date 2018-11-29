# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class UserStatsViewSet(common.DataMartViewSet):
    serializer_class = serializers.UserStatsSerializer
    queryset = models.UserStats.objects.all()
    filter_fields = ('country_name', 'month', 'last_modify_date')
