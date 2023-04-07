from etools_datamart.apps.mart.data import models

from .. import common
from .serializers import DataMartSerializer


class InterventionActivitySerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionActivity
        exclude = (
            "seen",
            "source_id",
        )


class InterventionActivityViewSet(common.DataMartViewSet):
    serializer_class = InterventionActivitySerializer
    queryset = models.InterventionActivity.objects.all()
