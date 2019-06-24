from rest_framework import serializers

from etools_datamart.api.endpoints import common
from etools_datamart.apps.data import models


class InterventionBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InterventionBudget
        exclude = ()


class InterventionBudgetSerializerPlain(serializers.ModelSerializer):
    class Meta:
        model = models.InterventionBudget
        exclude = ('fr_numbers_data', 'cp_outputs_data', 'partner_focal_points_data',
                   'sections_data', 'unicef_focal_points_data',
                   'partner_focal_points_data')


class InterventionBudgetViewSet(common.DataMartViewSet):
    serializer_class = InterventionBudgetSerializer
    queryset = models.InterventionBudget.objects.all()
    serializers_fieldsets = {'std': None,
                             'plain': InterventionBudgetSerializerPlain,

                             }
