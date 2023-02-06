from etools_datamart.apps.mart.data import models

from .. import common
from .serializers import DataMartSerializer


class InterventionReviewSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionReview
        exclude = ('seen', 'source_id',)


class InterventionReviewViewSet(common.DataMartViewSet):
    serializer_class = InterventionReviewSerializer
    queryset = models.InterventionReview.objects.all()
