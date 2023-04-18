from rest_framework import serializers

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.sources.etools.models import UsersCountry

from .. import common


class WorkspaceSerializer(DataMartSerializer):
    currency_code = serializers.SerializerMethodField()
    currency_name = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = UsersCountry
        exclude = (
            "local_currency",
            "vision_sync_enabled",
            "vision_last_synced",
            "initial_zoom",
        )

    def get_currency_name(self, obj):
        return getattr(obj.local_currency, "code", None)

    def get_currency_code(self, obj):
        return getattr(obj.local_currency, "name", None)


class EtoolsWorkspaceViewSet(common.APIReadOnlyModelViewSet):
    serializer_class = WorkspaceSerializer
    queryset = UsersCountry.objects.select_related("local_currency").exclude(schema_name__in=["public"])
