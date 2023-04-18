from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class SectionSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Section


class SectionViewSet(common.DataMartViewSet):
    serializer_class = SectionSerializer
    queryset = models.Section.objects.all()
    filter_fields = ("name", "alternate_name", "dashboard")
    ordering_fields = (
        "name",
        "alternate_name",
    )
