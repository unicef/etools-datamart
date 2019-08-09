from django.contrib.gis.db import models as geomodels
from django.contrib.gis.db.models.functions import Centroid
from django.db import models

from etools_datamart.apps.data.models.base import DataMartManager, DataMartModel
from etools_datamart.apps.etools.models import LocationsGatewaytype, LocationsLocation


class GatewayType(DataMartModel):
    name = models.CharField(db_index=True, max_length=64)
    admin_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('schema_name', 'name'),
                           ('schema_name', 'admin_level'))

    class Options:
        source = LocationsGatewaytype
        sync_deleted_records = lambda loader: False

        key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
                                          source_id=record.id)

    def __str__(self):
        return self.name


class LocationManager(DataMartManager):
    def batch_update_centroid(self):
        sql = '''UPDATE "%s" SET point = ST_Centroid(geom)
 WHERE point IS NULL ;''' % self.model._meta.db_table
        self.raw(sql)

    def update_centroid(self):
        for each in self.objects.annotate(cent=Centroid('geom')):
            each.point = each.cent
            each.save()


class Location(DataMartModel):
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

    class Meta:
        unique_together = ('schema_name', 'source_id')

    class Options:
        depends = (GatewayType,)
        source = LocationsLocation
        queryset = lambda: LocationsLocation.objects.order_by('-parent')
        last_modify_field = 'modified'
        # sync_deleted_records = False
        mapping = {'source_id': 'id',
                   # 'area_code': lambda loader, record: loader.context['country'].business_area_code,
                   'parent': '__self__',
                   'gateway': GatewayType
                   }

    def __str__(self):
        return self.name
