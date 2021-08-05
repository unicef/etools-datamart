from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class PseaAssessmentSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.PseaAssessment


class PseaAssessmentViewSet(DataMartViewSet):
    serializer_class = PseaAssessmentSerializer
    queryset = models.PseaAssessment.objects.all()


class PseaAnswerSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.PseaAnswer


class PseaAnswerViewSet(DataMartViewSet):
    serializer_class = PseaAnswerSerializer
    queryset = models.PseaAnswer.objects.all()
