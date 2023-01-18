from etools_datamart.apps.mart.data import models

from .. import common
from .serializers import DataMartSerializer


class InterventionManagementBudgetSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionManagementBudget
        exclude = ('seen', 'source_id',)


class InterventionBudgetMgmtViewSet(common.DataMartViewSet):
    serializer_class = InterventionManagementBudgetSerializer
    queryset = models.InterventionManagementBudget.objects.all()
