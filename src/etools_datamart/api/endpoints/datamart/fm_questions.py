from rest_framework import serializers

from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class FMQuestionSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMQuestion
        fields = "__all__"


class FMQuestionViewSet(DataMartViewSet):
    serializer_class = FMQuestionSerializer
    queryset = models.FMQuestion.objects.all()


class FMOntrackSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FMOntrack
        fields = "__all__"


class FMOntrackViewSet(DataMartViewSet):
    serializer_class = FMOntrackSerializer
    queryset = models.FMOntrack.objects.all()
