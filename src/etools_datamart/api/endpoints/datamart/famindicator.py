# -*- coding: utf-8 -*-
from month_field.rest_framework import MonthFilterBackend

from etools_datamart.apps.data import models

from . import serializers
from .. import common


class FAMIndicatorViewSet(common.APIReadOnlyModelViewSet):
    serializer_class = serializers.FAMIndicatorSerializer
    queryset = models.FAMIndicator.objects.all()
    filter_fields = ('country_name', )
    filter_backends = [MonthFilterBackend] + common.APIReadOnlyModelViewSet.filter_backends
