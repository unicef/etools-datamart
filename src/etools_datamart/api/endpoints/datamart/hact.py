# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from .. import common
from . import serializers


class HACTViewSet(common.DataMartViewSet):
    serializer_class = serializers.HACTSerializer
    queryset = models.HACT.objects.all()
    filter_fields = ('year', 'last_modify_date')
