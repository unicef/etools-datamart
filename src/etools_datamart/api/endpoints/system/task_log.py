# -*- coding: utf-8 -*-
from etools_datamart.apps.etl import models

from . import serializers
from .. import common


class TaskLogViewSet(common.APIReadOnlyModelViewSet):
    """

    """
    pagination_class = None
    serializer_class = serializers.TaskLogSerializer
    queryset = models.EtlTask.objects.all()
    filter_fields = ('task', 'table_name', 'result',
                     'last_success', 'last_failure')
