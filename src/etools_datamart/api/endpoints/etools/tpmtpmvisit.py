from rest_framework import serializers

from etools_datamart.api.endpoints import common
from etools_datamart.apps.sources.etools import models


class TpmTpmvisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TpmTpmvisit
        exclude = ()


class TpmTpmvisitViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = TpmTpmvisitSerializer
    queryset = models.TpmTpmvisit.objects.all()
