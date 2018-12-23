from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer

from etools_datamart.api.endpoints import common
from etools_datamart.apps.data import models


class LocationSerializerGeoJson(GeoFeatureModelSerializer):
    class Meta:
        model = models.Location
        exclude = ('schema_name', 'tree_id', 'lft', 'rght', 'level', 'source_id')
        geo_field = 'geom'


class LocationSerializerGIS(GeoModelSerializer):
    class Meta:
        model = models.Location
        exclude = ('schema_name', 'tree_id', 'lft', 'rght', 'level', 'source_id')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        exclude = ('schema_name', 'tree_id', 'lft', 'rght', 'level', 'source_id',
                   'geom', 'point', 'latitude', 'longitude')


class LocationViewSet(common.DataMartViewSet):
    serializer_class = LocationSerializer
    queryset = models.Location.objects.all()
    filter_fields = ('area_code', 'country_name', 'last_modify_date',
                     )
    serializers_fieldsets = {'std': None,
                             'light': ('country_name', 'area_code', 'p_code', 'name'),
                             'gis': LocationSerializerGIS,
                             'geo': LocationSerializerGeoJson,
                             }
