from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class WorkspaceSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Workspace


class WorkspaceViewSet(common.DataMartViewSet):
    serializer_class = WorkspaceSerializer
    queryset = models.Workspace.objects.exclude(schema_name__in=["public"])
