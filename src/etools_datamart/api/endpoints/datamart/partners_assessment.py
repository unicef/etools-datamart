from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class AssessmentSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Assessment


class PartnerAssessmentViewSet(common.DataMartViewSet):
    serializer_class = AssessmentSerializer
    queryset = models.Assessment.objects.all()
