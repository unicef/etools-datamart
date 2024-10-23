from django.contrib.gis.db import models as geomodels
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import FieldMonitoringSettingsLocationsite


class LocationsiteLoader(EtoolsLoader):
    def get_parent(self, record: FieldMonitoringSettingsLocationsite, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Location

        loc_fields = ["id", "name", "p_code", "level", "source_id", "admin_level", "admin_level_name"]

        try:
            instance = Location.objects.get(schema_name=self.context["country"].schema_name, source_id=record.parent.pk)
            return {
                "id": instance.pk,
                "name": instance.name,
                "p_code": instance.p_code,
                "admin_level": instance.admin_level,
                "source_id": instance.source_id,
                "location_type": instance.admin_level_name,
            }
        except Location.DoesNotExist:
            return {key: "N/A" for key in loc_fields}


class Locationsite(EtoolsDataMartModel):
    name = models.CharField(max_length=254)
    p_code = models.CharField(max_length=32)
    point = geomodels.PointField(blank=True, null=True)
    is_active = models.BooleanField()
    parent = models.JSONField(blank=True, null=True, default=dict)

    loader = LocationsiteLoader()

    class Options:
        source = FieldMonitoringSettingsLocationsite
        depends = (Location,)
        mapping = dict(
            parent="-",
        )
