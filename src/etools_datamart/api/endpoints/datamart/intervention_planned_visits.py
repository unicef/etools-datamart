from etools_datamart.apps.mart.data import models

from .. import common
from .serializers import DataMartSerializer


class InterventionPlannedVisitsSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionPlannedVisits
        exclude = ('seen', 'source_id',)


class InterventionPlannedVisitsViewSet(common.DataMartViewSet):
    serializer_class = InterventionPlannedVisitsSerializer
    queryset = models.InterventionPlannedVisits.objects.all()
