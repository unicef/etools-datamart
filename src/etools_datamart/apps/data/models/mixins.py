from django.db import models


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
                  })
    return ret


class LocationMixin(models.Model):
    location_source_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=254, blank=True, null=True)
    location_pcode = models.CharField(max_length=32, blank=True, null=True)
    location_level = models.IntegerField(blank=True, null=True)
    location_levelname = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        abstract = True
