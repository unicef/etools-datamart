from django.contrib.gis.db.models import MultiPolygonField, PointField
from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel
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
        # mapping = {'source_id': 'id',
        #            'area_code': lambda loader, record: loader.context['country'].business_area_code,
        #            'country_name': lambda loader, record: loader.context['country'].name,
        #            }


class Location(DataMartModel):
    name = models.CharField(max_length=254)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = PointField(blank=True, null=True)
    gateway = models.ForeignKey(GatewayType, models.DO_NOTHING)
    geom = MultiPolygonField(blank=True, null=True)
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        unique_together = ('schema_name', 'source_id')

    class Options:
        depends = (GatewayType,)
        # source = LocationsLocation
        queryset = lambda: LocationsLocation.objects.order_by('-parent')
        last_modify_field = 'modified'
        # sync_deleted_records = False
        mapping = {'source_id': 'id',
                   # 'area_code': lambda loader, record: loader.context['country'].business_area_code,
                   'parent': '__self__',
                   'gateway': GatewayType
                   }
