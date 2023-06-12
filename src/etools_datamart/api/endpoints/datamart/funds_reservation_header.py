from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class FundsReservationHeaderSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FundsReservationHeader


class FundsReservationHeaderViewSet(common.DataMartViewSet):
    serializer_class = FundsReservationHeaderSerializer
    queryset = models.FundsReservationHeader.objects.all()
    filter_fields = ("vendor_code", "fr_type", "start_date")
    search_fields = ("vendor_code", "fr_number")
