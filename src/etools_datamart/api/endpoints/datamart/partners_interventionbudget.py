from rest_framework import serializers

from etools_datamart.api.endpoints import common
from etools_datamart.apps.data import models


class InterventionBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InterventionBudget


class InterventionBudgetViewSet(common.DataMartViewSet):
    serializer_class = InterventionBudgetSerializer
    queryset = models.InterventionBudget.objects.all()
    serializers_fieldsets = {'std': None,
                             }
