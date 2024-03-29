from django import forms

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer

from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models


class LocationSerializerGeoJson(GeoFeatureModelSerializer):
    class Meta:
        model = models.Location
        exclude = ("schema_name", "tree_id", "lft", "rght", "level", "source_id")
        geo_field = "geom"


class LocationSerializerGIS(GeoModelSerializer):
    class Meta:
        model = models.Location
        exclude = ("schema_name", "tree_id", "lft", "rght", "level", "source_id")


class LocationSerializerPos(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        exclude = None
        fields = ("latitude", "longitude", "name", "point")


class LocationSerializer(serializers.ModelSerializer):
    geonameid = serializers.SerializerMethodField()

    class Meta:
        model = models.Location
        exclude = (
            "schema_name",
            "tree_id",
            "lft",
            "rght",
            "level",
            "source_id",
            "geom",
            "point",
            "latitude",
            "longitude",
        )

    def get_geonameid(self, obj):
        if obj.geoname:
            return obj.geoname.geoname_id
        return None


class LocationRamSerializer(serializers.ModelSerializer):
    geonameid = serializers.SerializerMethodField()

    class Meta:
        model = models.Location
        fields = (
            "id",
            "source_id",
            "name",
            "latitude",
            "longitude",
            "parent",
            "schema_name",
            "area_code",
            "p_code",
            "admin_level",
            "geonameid",
            "is_active",
            "last_modify_date",
            "created",
            "modified",
        )

    def get_geonameid(self, obj):
        if obj.geoname:
            return obj.geoname.geoname_id
        return None


class LocationViewSet(common.DataMartViewSet):
    serializer_class = LocationSerializer
    queryset = models.Location.objects.all()
    filter_fields = (
        "area_code",
        "country_name",
        "last_modify_date",
        "admin_level",
        "admin_level_name",
        "parent",
        "tree_id",
        "is_active",
    )
    serializers_fieldsets = {
        "std": None,
        "light": ("country_name", "area_code", "p_code", "name"),
        "gis": LocationSerializerGIS,
        "geo": LocationSerializerGeoJson,
        "latlng": LocationSerializerPos,
        "ram": LocationRamSerializer,
    }


class LocationSiteSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Locationsite


class LocationSiteViewSet(DataMartViewSet):
    serializer_class = LocationSiteSerializer
    queryset = models.Locationsite.objects.all()
