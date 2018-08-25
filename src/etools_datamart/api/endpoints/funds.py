# -*- coding: utf-8 -*-
from etools_datamart.apps.etools import models

from . import common
from .. import serializers


class GrantViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.GrantSerializer
    queryset = models.FundsGrant.objects.all()


class FundsreservationitemViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.FundsreservationitemSerializer
    queryset = models.FundsFundsreservationitem.objects.all()


class FundsReservationHeaderViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.FundsReservationHeaderSerializer
    queryset = models.FundsFundsreservationheader.objects.all()
