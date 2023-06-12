from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class FundsReservationItemSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FundsReservationItem


class FundsReservationItemViewSet(common.DataMartViewSet):
    serializer_class = FundsReservationItemSerializer
    queryset = models.FundsReservationItem.objects.all()
    filter_fields = ("fund_reservation_number",)
    search_fields = ("wbs", "grant_number", "fund", "line_item_text", "donor_code", "donor")
