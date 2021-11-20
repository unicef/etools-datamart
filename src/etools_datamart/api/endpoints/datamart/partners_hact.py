from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class PartnerSerializerFull(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.PartnerHact


class PartnerHactViewSet(common.DataMartViewSet):

    serializer_class = PartnerSerializerFull
    queryset = models.PartnerHact.objects.all()
    ordering_fields = ("id", "name")
