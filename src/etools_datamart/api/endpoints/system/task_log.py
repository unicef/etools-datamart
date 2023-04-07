from etools_datamart.apps.etl import models

from .. import common
from . import serializers


class MonitorViewSet(common.APIReadOnlyModelViewSet):
    """ """

    pagination_class = None
    serializer_class = serializers.TaskLogSerializer
    queryset = models.EtlTask.objects.all()
    filter_fields = ("task", "table_name", "result", "last_success", "last_failure")
