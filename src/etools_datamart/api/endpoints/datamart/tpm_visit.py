# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class TPMVisitSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.TPMVisit


class TPMVisitViewSet(common.DataMartViewSet):
    serializer_class = TPMVisitSerializer
    queryset = models.TPMVisit.objects.all()
    filter_fields = ('status', 'date_of_assigned', 'date_of_tpm_accepted',
                     'date_of_tpm_rejected')
    ordering_fields = ("id", "created",)
