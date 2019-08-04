# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class HACTHistorySerializer(DataMartSerializer):
    # last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    class Meta(DataMartSerializer.Meta):
        model = models.HACTHistory


class HACTHistoryViewSet(common.DataMartViewSet):
    serializer_class = HACTHistorySerializer
    queryset = models.HACTHistory.objects.all()
    filter_fields = ('year', 'last_modify_date')
