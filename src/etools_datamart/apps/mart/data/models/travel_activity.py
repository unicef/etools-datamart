import datetime

from django.conf import settings
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.sources.etools.models import T2FTravelactivity


class TravelActivityLoader(EtoolsLoader):
    def get_queryset(self):
        return (
            self.config.source.objects.filter(date__year__gte=datetime.datetime.now().year - settings.YEAR_DELTA)
            .select_related("partner", "partnership", "primary_traveler", "result")
            .prefetch_related("travels", "locations")
        )

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for record in qs.order_by("id", "-date"):
            record.travel = record.travels.order_by("id").first()
            if record.travel:
                if record.locations.exists():
                    for location in record.locations.order_by("id"):
                        record.location = location
                        filters = self.config.key(self, record)
                        values = self.get_values(record)
                        op = self.process_record(filters, values)
                        self.increment_counter(op)
                else:
                    record.location = None
                    filters = self.config.key(self, record)
                    values = self.get_values(record)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)


class TravelActivity(LocationMixin, EtoolsDataMartModel):
    travel_reference_number = models.CharField(max_length=200, blank=True, null=True)
    travel_type = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    partner_name = models.CharField(max_length=200, blank=True, null=True)
    partnership_number = models.CharField(max_length=200, blank=True, null=True)
    primary_traveler = models.CharField(max_length=200, blank=True, null=True)

    # internal
    source_travel_id = models.IntegerField(null=True)
    source_partner_id = models.IntegerField(null=True)
    source_partnership_id = models.IntegerField(null=True)

    result_name = models.TextField(max_length=200, blank=True, null=True)
    result_code = models.CharField(max_length=200, blank=True, null=True)
    result_type = models.CharField(max_length=200, blank=True, null=True)

    loader = TravelActivityLoader()

    class Meta:
        unique_together = ("schema_name", "source_id", "travel_reference_number", "location_source_id")

    class Options:
        # depends = (Travel, Location)
        source = T2FTravelactivity
        last_modify_field = None
        sync_deleted_records = lambda a: False
        key = lambda loader, record: dict(
            country_name=loader.context["country"].name,
            schema_name=loader.context["country"].schema_name,
            source_id=record.id,
            location_source_id=record.location.id if record.location else None,
        )
        mapping = add_location_mapping(
            {
                "source_travel_id": "travel.id",
                "source_partner_id": "partner.id",
                "source_partnership_id": "partnership.id",
                # 'location_source_id': 'location.id',
                # 'location_name': 'location.name',
                # 'location_pcode': 'location.p_code',
                # 'location_level': 'location.admin_level',
                # 'location_levelname': 'location.admin_level_name',
                "travel_reference_number": "travel.reference_number",
                "primary_traveler": "primary_traveler.email",
                "partner_name": "partner.organization.name",
                "partnership_number": "partnership.number",
                "result_name": "result.name",
                "result_code": "result.code",
                "result_type": "result.result_type.name",
            }
        )
