from etools_datamart.apps.mart.data import models

from .. import common
from .serializers import DataMartSerializer


class InterventionCountryProgrammeSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionCountryProgramme
        exclude = (
            "seen",
            "source_id",
        )


class InterventionCPViewSet(common.DataMartViewSet):
    serializer_class = InterventionCountryProgrammeSerializer
    queryset = models.InterventionCountryProgramme.objects.all()
