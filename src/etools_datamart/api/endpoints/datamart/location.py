from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer

from etools_datamart.api.endpoints import common
from etools_datamart.apps.mart.data import models


class LocationSerializerGeoJson(GeoFeatureModelSerializer):
    class Meta:
        model = models.Location
        exclude = ('schema_name', 'tree_id', 'lft', 'rght', 'level', 'source_id')
        geo_field = 'geom'


class LocationSerializerGIS(GeoModelSerializer):
    class Meta:
        model = models.Location
        exclude = ('schema_name', 'tree_id', 'lft', 'rght', 'level', 'source_id')


class LocationSerializerPos(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        exclude = None
        fields = ('latitude', 'longitude', 'name', 'point')


class LocationSerializer(serializers.ModelSerializer):
    geonameid = serializers.SerializerMethodField()

    class Meta:
        model = models.Location
        exclude = ('schema_name', 'tree_id', 'lft', 'rght', 'level', 'source_id',
                   'geom', 'point', 'latitude', 'longitude')

    def get_geonameid(self, obj):
        if obj.geoname:
            return geoname.geoname_id
        return None


class LocationViewSet(common.DataMartViewSet):
    serializer_class = LocationSerializer
    queryset = models.Location.objects.all()
    filter_fields = ('area_code', 'country_name', 'last_modify_date',
                     )
    serializers_fieldsets = {'std': None,
                             'light': ('country_name', 'area_code', 'p_code', 'name'),
                             'gis': LocationSerializerGIS,
                             'geo': LocationSerializerGeoJson,
                             'latlng': LocationSerializerPos,
                             }
