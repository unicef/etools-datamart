from django.db import models
from django.db.models import JSONField
from django.forms import model_to_dict

from etools_datamart.sentry import process_exception

from .location import Location


def extend(base, other):
    ret = dict(base)
    ret.update(**other)
    return ret


def _get_location(loader, record):
    try:
        if record.location:
            return Location.objects.filter(
                source_id=record.location.id, schema_name=loader.context["country"].schema_name
            ).first()
    except Exception as e:
        process_exception(e)
    return None


def add_location_mapping(base):
    ret = dict(base)
    ret.update(
        **{
            "location_source_id": "location.id",
            "location_name": "location.name",
            "location_pcode": "location.p_code",
            "location_level": "location.admin_level",
            "location_levelname": "location.admin_level_name",
            "location": _get_location,
        }
    )
    return ret


class LocationMixin(models.Model):
    location_source_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=254, blank=True, null=True)
    location_pcode = models.CharField(max_length=32, blank=True, null=True)
    location_level = models.IntegerField(blank=True, null=True)
    location_levelname = models.CharField(max_length=80, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class NestedLocationLoaderMixin:
    location_m2m_field = None

    def get_locations(self, record, values: dict, **kwargs):
        location_list = list(
            Location.objects.filter(
                source_id__in=list(getattr(record, self.location_m2m_field).values_list("id", flat=True)),
                schema_name=self.context["country"].schema_name,
            )
            .values("id", "name", "p_code", "admin_level", "admin_level_name", "latitude", "longitude")
            .order_by("id")
        )
        values["locations_data"] = location_list

        return ", ".join([l["name"] for l in location_list])


class NestedLocationMixin(models.Model):
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    class Meta:
        abstract = True
