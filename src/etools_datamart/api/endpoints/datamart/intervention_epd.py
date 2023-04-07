from etools_datamart.apps.mart.data import models

from .. import common
from .serializers import DataMartSerializer


class InterventionEPDSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionEPD
        exclude = (
            "seen",
            "source_id",
        )


class InterventionEPDViewSet(common.DataMartViewSet):
    serializer_class = InterventionEPDSerializer
    queryset = models.InterventionEPD.objects.all()
