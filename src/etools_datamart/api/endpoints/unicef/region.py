from unicef_realm import models

from .. import common
from . import serializers


class RegionViewSet(common.APIReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.RegionSerializer
    queryset = models.Region.objects.all()
    filter_fields = ('task', 'table_name', 'result',
                     'last_success', 'last_failure')
