from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class OfficeSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Office
        exclude = ('seen',)


class OfficeViewSet(common.DataMartViewSet):
    serializer_class = OfficeSerializer
    queryset = models.Office.objects.all()
