# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.etools import models


class TravelViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.TravelSerializer
    queryset = models.T2FTravel.objects.all()
