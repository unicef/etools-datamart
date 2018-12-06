# -*- coding: utf-8 -*-
from unicef_security import models

from . import serializers
from .. import common


class RegionViewSet(common.APIReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.RegionSerializer
    queryset = models.Region.objects.all()
    filter_fields = ('task', 'table_name', 'result',
                     'last_success', 'last_failure')
