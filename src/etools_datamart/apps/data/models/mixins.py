from django.contrib.postgres.fields import JSONField
from django.db import models

from crashlog.middleware import process_exception

from .location import Location


def extend(base, other):
    ret = dict(base)
    ret.update(**other)
    return ret


def _get_location(loader, record):
    try:
        if record.location:
            return Location.objects.filter(source_id=record.location.id,
                                           schema_name=loader.context[
                                               'country'].schema_name).first()
    except Exception as e:
        process_exception(e)
    return None


def add_location_mapping(base):
    ret = dict(base)
    ret.update(**{'location_source_id': 'location.id',
                  'location_name': 'location.name',
                  'location_pcode': 'location.p_code',
                  'location_level': 'location.level',
                  'location_levelname': 'location.gateway.name',
                  'location': _get_location
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


class NestedLocationLoaderMixin:
    location_m2m_field = None

    def get_locations(self, record, values: dict, **kwargs):
        locs = []
        locations = getattr(record, self.location_m2m_field)
        for location in locations.select_related('gateway').order_by('id'):
            location_data = dict(
                source_id=location.id,
                name=location.name,
                pcode=location.p_code,
                level=location.level,
                levelname=location.gateway.name,
                latitude=None,
                longitude=None
            )
            try:
                loc = Location.objects.get(source_id=location.id,
                                           schema_name=self.context['country'].schema_name)
                location_data["latitude"] = loc.latitude
                location_data["longitude"] = loc.longitude
            except Exception as e:
                process_exception(e)

            locs.append(location_data)
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])


class NestedLocationMixin(models.Model):
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    class Meta:
        abstract = True
