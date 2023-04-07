from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class PDIndicatorSerializer(DataMartSerializer):
    class Meta:
        model = models.PDIndicator
        fields = "__all__"


class PDIndicatorViewSet(common.DataMartViewSet):
    serializer_class = PDIndicatorSerializer
    queryset = models.PDIndicator.objects.all()
