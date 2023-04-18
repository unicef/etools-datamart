from datetime import datetime

from month_field.rest_framework import MonthFilterBackend
from rest_framework.fields import SerializerMethodField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class UserStatsSerializer(DataMartSerializer):
    month = SerializerMethodField(help_text="---")

    class Meta(DataMartSerializer.Meta):
        model = models.UserStats
        read_only = [
            "last_modify_date",
        ]

    def get_month(self, obj):
        return datetime.strftime(obj.month._date, "%b %Y")


class UserStatsViewSet(common.DataMartViewSet):
    serializer_class = UserStatsSerializer
    filter_backends = [MonthFilterBackend] + common.DataMartViewSet.filter_backends
    queryset = models.UserStats.objects.all()
    filter_fields = ("last_modify_date",)
    serializers_fieldsets = {"std": None}
