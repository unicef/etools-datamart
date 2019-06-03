# -*- coding: utf-8 -*-
# import django_filters
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class TPMActivitySerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.TPMActivity


class TPMActivityViewSet(common.DataMartViewSet):
    serializer_class = TPMActivitySerializer
    queryset = models.TPMActivity.objects.all()
    filter_fields = ('date', 'is_pv', 'visit_status', 'source_id')
    ordering_fields = ("id", "created",)
