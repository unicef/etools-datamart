# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class HACTViewSet(common.APIReadOnlyModelViewSet):
    serializer_class = serializers.HACTSerializer
    queryset = models.HACT.objects.all()
    filter_fields = ('country_name', 'month')
