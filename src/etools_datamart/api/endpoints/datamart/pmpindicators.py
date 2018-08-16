# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from .. import common
from . import serializers


class PMPIndicatorsViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.PMPIndicatorsSerializer
    queryset = models.PMPIndicators.objects.all()
