# -*- coding: utf-8 -*-
from etools_datamart.apps.etools import models

from . import common
from .. import serializers


class FTravelViewSet(common.MultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.FTravelSerializer
    queryset = models.T2FTravel.objects.all()
