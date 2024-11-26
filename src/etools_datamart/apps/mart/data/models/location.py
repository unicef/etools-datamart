from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.db.models.functions import Centroid
from django.db import connection, models

import requests

from etools_datamart.apps.core.models import DataMartManager, DataMartQuerySet
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import LocationsLocation

from ..loader import EtoolsLoader

"""
-- Set country; 
SET search_path = public,<country>
-- Get count for paging calculation;
SELECT COUNT(*) AS "__count" FROM "locations_location"
-- Paged fetch;
SELECT '<country>' AS __schema, 
       "locations_location"."id",
       "locations_location"."name",
       "locations_location"."latitude",
       "locations_location"."longitude",
       "locations_location"."p_code",
       "locations_location"."point",
       "locations_location"."geom",
       "locations_location"."level",
       "locations_location"."lft",
       "locations_location"."parent_id",
       "locations_location"."rght",
       "locations_location"."tree_id",
       "locations_location"."created",
       "locations_location"."modified",
       "locations_location"."is_active",
       "locations_location"."admin_level",
       "locations_location"."admin_level_name" 
FROM "locations_location" 
ORDER BY "locations_location"."id" ASC
"""


class LocationQuerySet(DataMartQuerySet):
    def batch_update_centroid(self):
        sql = """UPDATE "{0}" SET point = ST_Centroid(geom::geometry),
latitude = ST_Y(ST_Centroid(geom::geometry)),
longitude = ST_X(ST_Centroid(geom::geometry))
WHERE point IS NULL AND geom IS NOT NULL;
UPDATE "{0}" SET latitude = NULL, longitude = NULL WHERE point IS NULL;
""".format(
            self.model._meta.db_table
        )
        with connection.cursor() as cursor:
            cursor.execute(sql)

        # need to update geoname
        for record in (
            super()
            .filter(
                latitude__isnull=False,
                longitude__isnull=False,
            )
            .all()
        ):
            geoname, __ = GeoName.objects.get_or_create(
                lat=record.latitude,
                lng=record.longitude,
            )
            if record.geoname != geoname:
                record.geoname = geoname
                record.save()

    def update_centroid(self):
        clone = self._chain()
        for each in clone.annotate(cent=Centroid("geom")):
            each.point = each.cent
            each.latitude = each.point.y
            each.longitude = each.point.x
            each.geoname, __ = GeoName.objects.get_or_create(
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
            pass
            # Location.objects.batch_update_centroid()


class Location(EtoolsDataMartModel):
    name = models.CharField(max_length=254, db_index=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = geomodels.PointField(blank=True, null=True)
    admin_level = models.SmallIntegerField(blank=True, null=True)
    admin_level_name = models.CharField(max_length=64, blank=True, null=True)
    geom = geomodels.MultiPolygonField(geography=True, blank=True, null=True)
    geoname = models.ForeignKey("GeoName", models.DO_NOTHING, blank=True, null=True)
    level = models.IntegerField(db_index=True)
    lft = models.IntegerField()
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_active = models.BooleanField()

    objects = LocationManager()
    loader = LocationLoader()

    class Meta:
        unique_together = ("schema_name", "source_id")
        ordering = ("name",)

    class Options:
        source = LocationsLocation
        queryset = lambda: LocationsLocation.objects.order_by("-parent")
        last_modify_field = "modified"
        exclude_from_compare = ["latitude", "longitude", "point", "geoname"]
        # sync_deleted_records = False
        mapping = {
            "source_id": "id",
            "parent": "__self__",
        }

    def __str__(self):
        return self.name


class GeoNameLimitException(Exception):
    # GeoName requests have reached their limit
    pass


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

    class Meta:
        unique_together = ("lat", "lng")

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lng})"

    def sync(self):
        # store geo names pulled from http://api.geonames.org
        # Using lat and lng get geoname data with
        # http://api.geonames.org/findNearbyJSON?lat=47.3&lng=9&username=ntrncic
        payload = {
            "lat": self.lat,
            "lng": self.lng,
            "username": settings.GEONAMES_USERNAME,
        }
        res = requests.get(
            settings.GEONAMES_URL,
            params=payload,
            timeout=30,
        )
        geonames = res.json()
        # check for exception
        if "status" in geonames:
            if geonames["status"]["value"] in [18, 19, 20]:
                raise GeoNameLimitException
            return None

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
        try:
            geoname = geonames["geonames"][0]
        except IndexError:
            return None
        # to prevent unique exception as lat/lng
        # returned in response may be altered
        geo, __ = GeoName.objects.get_or_create(
            lat=geoname.get("lat"),
            lng=geoname.get("lng"),
        )
        for k, f in mapping:
            try:
                setattr(geo, k, geoname.get(f))
            except AttributeError:
                return None
        if self != geo:
            # geoname wioth lat/lng already exists
            # update all related locations to existing geoname
            # and delete this instance
            Location.objects.filter(geoname=self).update(geoname=geo)
            self.delete()
        geo.save()
