from xml.etree import ElementTree

from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.db.models.functions import Centroid
from django.db import connection, models

import requests

from etools_datamart.apps.core.models import DataMartManager, DataMartQuerySet
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import LocationsGatewaytype, LocationsLocation

from ..loader import EtoolsLoader


class GatewayType(EtoolsDataMartModel):
    name = models.CharField(db_index=True, max_length=64)
    admin_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('schema_name', 'source_id'),
                           )

    class Options:
        source = LocationsGatewaytype
        sync_deleted_records = lambda loader: False

        # key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
        #                                   source_id=record.id)

    def __str__(self):
        return self.name


class LocationQuerySet(DataMartQuerySet):
    def batch_update_centroid(self):
        sql = '''UPDATE "{0}" SET point = ST_Centroid(geom),
latitude = ST_Y(ST_Centroid(geom)),
longitude = ST_X(ST_Centroid(geom))
WHERE point IS NULL AND geom IS NOT NULL;
UPDATE "{0}" SET latitude = NULL, longitude = NULL WHERE point IS NULL;
'''.format(self.model._meta.db_table)
        with connection.cursor() as cursor:
            cursor.execute(sql)

        # need to update geoname
        for record in super().filter(
                latitude__isnull=False,
                longitude__isnull=False,
        ).all():
            geoname = GeoName.objects.get_or_add(
                lat=record.latitude,
                lng=record.longitude,
            )
            if record.geoname != geoname:
                record.geoname = geoname
                record.save()

    def update_centroid(self):
        clone = self._chain()
        for each in clone.annotate(cent=Centroid('geom')):
            each.point = each.cent
            each.latitude = each.point.y
            each.longitude = each.point.x
            each.geoname = GeoName.objects.get_or_add(
                lat=each.point.y,
                lng=each.point.x,
            )
            each.save()


class LocationManager(DataMartManager.from_queryset(LocationQuerySet)):
    pass


class LocationLoader(EtoolsLoader):

    def load(self, **kwargs):
        try:
            return super().load(**kwargs)
        finally:
            Location.objects.batch_update_centroid()


class Location(EtoolsDataMartModel):
    name = models.CharField(max_length=254, db_index=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = geomodels.PointField(blank=True, null=True)
    gateway = models.ForeignKey(GatewayType, models.DO_NOTHING, blank=True, null=True)
    geom = geomodels.MultiPolygonField(blank=True, null=True)
    geoname = models.ForeignKey("GeoName", models.DO_NOTHING, blank=True, null=True)
    level = models.IntegerField(db_index=True)
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_active = models.BooleanField()

    objects = LocationManager()
    loader = LocationLoader()

    class Meta:
        unique_together = ('schema_name', 'source_id')
        ordering = ("name",)

    class Options:
        depends = (GatewayType,)
        source = LocationsLocation
        queryset = lambda: LocationsLocation.objects.order_by('-parent')
        last_modify_field = 'modified'
        exclude_from_compare = ['latitude', 'longitude', 'point', 'geoname']
        # sync_deleted_records = False
        mapping = {'source_id': 'id',
                   # 'area_code': lambda loader, record: loader.context['country'].business_area_code,
                   'parent': '__self__',
                   'gateway': GatewayType,
                   }

    def __str__(self):
        return self.name


# store geo names pulled from http://api.geonames.org
# Using lat and lng get geoname data with
# http://api.geonames.org/findNearby?lat=47.3&lng=9&username=ntrncic
class GeoNameManager(models.Manager):
    def get_or_add(self, lat, lng):
        # check if we have a matching lat, lng record
        # if so, return that record
        # otherwise create a new record based on results
        # of request to geonames.org
        if not lat or not lng:
            return None
        try:
            geoname = self.get_queryset().get(lat=lat, lng=lng)
        except GeoName.DoesNotExist:
            payload = {
                "lat": lat,
                "lng": lng,
                "username": settings.GEONAMES_USERNAME,
            }
            res = requests.get(
                settings.GEONAMES_URL,
                params=payload,
                timeout=settings.REQUEST_TIMEOUT,
            )
            geoname = ElementTree.fromstring(res.content)[0]
            mapping = [
                ("toponym_name", "toponymName"),
                ("name", "name"),
                ("lat", "lat"),
                ("lng", "lng"),
                ("geoname_id", "geonameId"),
                ("country_code", "countryCode"),
                ("country_name", "countryName"),
                ("fcl", "fcl"),
                ("fcode", "fcode"),
                ("distance", "distance"),
            ]
            data = {}
            for k, f in mapping:
                try:
                    data[k] = geoname.find(f).text
                except AttributeError:
                    return None
            lat = data.pop("lat")
            lng = data.pop("lng")
            geoname, __ = GeoName.objects.get_or_create(
                lat=lat,
                lng=lng,
                defaults=data,
            )
        return geoname


class GeoName(models.Model):
    toponym_name = models.CharField(max_length=254, null=True)
    name = models.CharField(max_length=254, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    geoname_id = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=20, null=True)
    country_name = models.CharField(max_length=150, null=True)
    fcl = models.CharField(max_length=50, null=True)
    fcode = models.CharField(max_length=50, null=True)
    distance = models.FloatField(null=True)

    objects = GeoNameManager()

    class Meta:
        unique_together = ('lat', 'lng')

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lng})"
