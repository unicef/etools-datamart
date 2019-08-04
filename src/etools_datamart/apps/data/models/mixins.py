from django.contrib.postgres.fields import JSONField
from django.db import models

from .location import Location


def extend(base, other):
    ret = dict(base)
    ret.update(**other)
    return ret


def add_location_mapping(base):
    ret = dict(base)
    ret.update(**{'location_source_id': 'location.id',
                  'location_name': 'location.name',
                  'location_pcode': 'location.p_code',
                  'location_level': 'location.level',
                  'location_levelname': 'location.gateway.name',
                  'location': lambda loader, record: Location.objects.filter(source_id=record.id,
                                                                             schema_name=loader.context[
                                                                                 'country'].schema_name).first(),

                  })
    return ret


class LocationMixin(models.Model):
    location_source_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=254, blank=True, null=True)
    location_pcode = models.CharField(max_length=32, blank=True, null=True)
    location_level = models.IntegerField(blank=True, null=True)
    location_levelname = models.CharField(max_length=32, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class LocationLoadertMixin:
    location_m2m_field = 'locations'

    def get_locations(self, original, values: dict, **kwargs):
        locs = []
        locations = getattr(original, self.location_m2m_field)
        for location in locations.select_related('gateway').order_by('id'):
            locs.append(dict(
                source_id=location.id,
                name=location.name,
                pcode=location.p_code,
                level=location.level,
                levelname=location.gateway.name
            ))
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])


class LocationInlineMixin(models.Model):
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    class Meta:
        abstract = True
