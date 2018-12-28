from django.contrib.gis.db.models import MultiPolygonField, PointField
from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import LocationsGatewaytype, LocationsLocation


class GatewayType(DataMartModel):
    name = models.CharField(db_index=True, max_length=64)
    admin_level = models.SmallIntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('schema_name', 'name'),
                           ('schema_name', 'admin_level'))

    class Options:
        source = LocationsGatewaytype
        key = lambda country, record: dict(schema_name=country.schema_name,
                                           name=record.name)
        mapping = {'source_id': 'id',
                   'area_code': lambda country, record: country.business_area_code,
                   }


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

    source_id = models.IntegerField(blank=True, null=True)

    class Options:
        depends = (GatewayType,)
        # source = LocationsLocation
        queryset = lambda: LocationsLocation.objects.order_by('-parent')

        mapping = {'source_id': 'id',
                   'area_code': lambda country, record: country.business_area_code,
                   'parent': '__self__',
                   'gateway': GatewayType
                   }
