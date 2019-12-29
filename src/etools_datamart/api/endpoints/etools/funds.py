# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.sources.etools import models


class EtoolsGrantViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.EToolsGrantSerializer
    queryset = models.FundsGrant.objects.all()


class EtoolsFundsreservationitemViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.EToolsFundsreservationitemSerializer
    queryset = models.FundsFundsreservationitem.objects.all()


class EtoolsFundsReservationHeaderViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.EToolsFundsReservationHeaderSerializer
    queryset = models.FundsFundsreservationheader.objects.all()
