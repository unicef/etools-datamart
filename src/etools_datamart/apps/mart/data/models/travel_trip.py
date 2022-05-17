from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.enrichment.consts import TravelTripConsts
from etools_datamart.apps.sources.etools.models import TravelTrip

from .base import EtoolsDataMartModel


class TripLoader(EtoolsLoader):
    def get_attachments(self, record, values, **kwargs):
        return ",\n".join(list(map(lambda x: ":".join(x),
                                   record.T2FTravelattachment_travel.values_list('type', 'file'))))


class TravelTrip(EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True, db_index=True)
    modified = models.DateTimeField(blank=True, null=True, db_index=True)
    reference_number = models.CharField(blank=True, null=True, max_length=12)
    status = models.CharField(max_length=50, choices=TravelTripConsts.CHOICES, db_index=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)

    office_name = models.CharField(max_length=254, blank=True, null=True, db_index=True)
    section_name = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    supervisor_email = models.CharField(max_length=200, blank=True, null=True)
    traveler_email = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    user_info_text = models.JSONField()
    additional_notes = models.TextField(blank=True, null=True)
    not_as_planned = models.BooleanField(blank=True, null=True)

    attachments = models.TextField(blank=True, null=True)

    loader = TripLoader()

    class Meta:
        unique_together = ('schema_name', 'reference_number')

    class Options:
        source = TravelTrip
        key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
                                          reference_number=record.reference_number)

        mapping = dict(office_name='office.name',
                       section_name='section.name',
                       supervisor_email='supervisor.email',
                       traveler_email='traveler.email')
