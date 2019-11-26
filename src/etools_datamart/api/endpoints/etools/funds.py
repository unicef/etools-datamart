# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.sources.etools import models


class GrantViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.GrantSerializer
    queryset = models.FundsGrant.objects.all()


class FundsreservationitemViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.FundsreservationitemSerializer
    queryset = models.FundsFundsreservationitem.objects.all()


class FundsReservationHeaderViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.FundsReservationHeaderSerializer
    queryset = models.FundsFundsreservationheader.objects.all()
