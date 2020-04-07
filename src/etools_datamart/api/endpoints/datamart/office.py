from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class OfficeSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Office


class OfficeViewSet(common.DataMartViewSet):
    serializer_class = OfficeSerializer
    queryset = models.Office.objects.all()
