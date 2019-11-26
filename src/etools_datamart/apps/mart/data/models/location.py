from django.contrib.gis.db import models as geomodels
from django.contrib.gis.db.models.functions import Centroid
from django.db import connection, models
from django.db.models.manager import BaseManager

from etools_datamart.apps.core.models import DataMartQuerySet
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

    def update_centroid(self):
        clone = self._chain()
        for each in clone.annotate(cent=Centroid('geom')):
            each.point = each.cent
            each.latitude = each.point.y
            each.longitude = each.point.x
            each.save()


class LocationManager(BaseManager.from_queryset(LocationQuerySet)):
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

    class Options:
        depends = (GatewayType,)
        source = LocationsLocation
        queryset = lambda: LocationsLocation.objects.order_by('-parent')
        last_modify_field = 'modified'
        exclude_from_compare = ['latitude', 'longitude', 'point']
        # sync_deleted_records = False
        mapping = {'source_id': 'id',
                   # 'area_code': lambda loader, record: loader.context['country'].business_area_code,
                   'parent': '__self__',
                   'gateway': GatewayType
                   }

    def __str__(self):
        return self.name
