# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class HACTAggreagateSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.HACT


class HACTAggreagateViewSet(common.DataMartViewSet):
    serializer_class = HACTAggreagateSerializer
    queryset = models.HACT.objects.all()
    filter_fields = ('year', 'last_modify_date')
