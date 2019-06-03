# -*- coding: utf-8 -*-
from unicef_security import models

from .. import common
from . import serializers


class BusinessAreaViewSet(common.APIReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.BusinessAreaSerializer
    queryset = models.BusinessArea.objects.all()
    filter_fields = ('code', 'name', 'long_name',
                     'region', 'country', 'last_modify_date')
