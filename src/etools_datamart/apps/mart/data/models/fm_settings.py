from django.contrib.gis.db import models as geomodels
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import FieldMonitoringSettingsLocationsite


class LocationsiteLoader(EtoolsLoader):
    """
    --
    SET search_path = public,##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "field_monitoring_settings_locationsite";

    -- field_monitoring_settings_locationsite entries for the page
    SELECT '##COUNTRY##' AS __schema,
           "field_monitoring_settings_locationsite"."id",
           "field_monitoring_settings_locationsite"."created",
           "field_monitoring_settings_locationsite"."modified",
           "field_monitoring_settings_locationsite"."name",
           "field_monitoring_settings_locationsite"."p_code",
           "field_monitoring_settings_locationsite"."point",
           "field_monitoring_settings_locationsite"."is_active",
           "field_monitoring_settings_locationsite"."parent_id"
    FROM "field_monitoring_settings_locationsite"
    ORDER BY "field_monitoring_settings_locationsite"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    -- Location entries for the page
    SELECT '##COUNTRY##' AS __schema,
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
    WHERE "locations_location"."id"  IN (## LIST OF "field_monitoring_settings_locationsite"."parent_id" IN THE PAGE##) ;
    """

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
    # from etools_datamart.apps.mart.data.models import Location

    name = models.CharField(max_length=254)
    p_code = models.CharField(max_length=32)
    point = geomodels.PointField(blank=True, null=True)
    is_active = models.BooleanField()
    parent = models.JSONField(blank=True, null=True, default=dict)

    loader = LocationsiteLoader()

    class Options:
        source = FieldMonitoringSettingsLocationsite
        depends_as_str = ("etools_datamart.apps.mart.data.models.Location",)
        mapping = dict(
            parent="-",
        )
