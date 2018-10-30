# -*- coding: utf-8 -*-
from etools_datamart.api import serializers
from etools_datamart.api.endpoints import common
from etools_datamart.apps.etools import models


class FTravelViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.FTravelSerializer
    queryset = models.T2FTravel.objects.all()
