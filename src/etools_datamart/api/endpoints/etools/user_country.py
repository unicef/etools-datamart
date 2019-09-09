from rest_framework import serializers

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data.models import Office
from etools_datamart.apps.etools.models import UsersCountry

from .. import common


class WorkspaceSerializer(DataMartSerializer):
    currency_code = serializers.SerializerMethodField()
    currency_name = serializers.SerializerMethodField()

    class Meta(DataMartSerializer.Meta):
        model = UsersCountry
        exclude = ('local_currency', 'vision_sync_enabled', 'vision_last_synced',
                   'initial_zoom',)

    def get_currency_name(self, obj):
        return getattr(obj.local_currency, 'code', None)

    def get_currency_code(self, obj):
        return getattr(obj.local_currency, 'name', None)


class WorkspaceSerializerExt(WorkspaceSerializer):
    offices = serializers.SerializerMethodField()

    def get_offices(self, obj):
        ret = []
        for o in Office.objects.filter(countries_data__short_code=obj.country_short_code):
            ret.append({'name': o.name,
                        'zonal_chief_email': o.zonal_chief_email,
                        'id': o.id})
        return ret


class WorkspaceViewSet(common.APIReadOnlyModelViewSet):
    serializer_class = WorkspaceSerializer
    queryset = UsersCountry.objects.select_related('local_currency').exclude(schema_name__in=['public'])
    serializers_fieldsets = {'std': None,
                             'ext': WorkspaceSerializerExt
                             }
