from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class FMQuestionSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMQuestion


class FMQuestionViewSet(DataMartViewSet):
    serializer_class = FMQuestionSerializer
    queryset = models.FMQuestion.objects.all()


class FMOntrackSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMOntrack


class FMOntrackViewSet(DataMartViewSet):
    serializer_class = FMOntrackSerializer
    queryset = models.FMOntrack.objects.all()


class FMOptionsSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMOptions


class FMOptionsViewSet(DataMartViewSet):
    serializer_class = FMOptionsSerializer
    queryset = models.FMOptions.objects.all()
