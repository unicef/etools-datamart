from django.db import models
from django.utils.functional import cached_property

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.enrichment.consts import TravelTripConsts
from etools_datamart.apps.sources.etools.models import DjangoContentType, TravelTrip, UnicefAttachmentsAttachment

from .base import EtoolsDataMartModel


class TravelTripLoader(EtoolsLoader):
    @cached_property
    def _ct(self):
        return DjangoContentType.objects.get(app_label='travel',
                                             model='trip')

    def get_attachments(self, record, values, **kwargs):
        attachments = (UnicefAttachmentsAttachment.objects
                       .select_related('file_type')
                       .filter(object_id=record.id,
                               code='travel_docs',
                               content_type=self._ct,
                               ).order_by('id'))
        ret = []
        for a in attachments:
            ret.append(dict(
                file=a.file,
                file_type=a.file_type.name,
                code=a.code,
            ))
        return ", ".join([a.file for a in attachments])


class TravelTrip(EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True, db_index=True)
    modified = models.DateTimeField(blank=True, null=True, db_index=True)
    reference_number = models.CharField(blank=True, null=True, max_length=100)
    status = models.CharField(max_length=30, choices=TravelTripConsts.CHOICES, db_index=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)

    office_name = models.CharField(max_length=254, blank=True, null=True, db_index=True)
    section_name = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    supervisor_email = models.CharField(max_length=200, blank=True, null=True)
    traveler_email = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    user_info_text = models.JSONField(default=dict, blank=True)
    additional_notes = models.TextField(blank=True, null=True)
    not_as_planned = models.BooleanField(blank=True, null=True)

    attachments = models.TextField(blank=True, null=True)

    loader = TravelTripLoader()

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
