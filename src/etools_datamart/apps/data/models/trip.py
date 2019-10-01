from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.translation import gettext as _

from dynamic_serializer.core import get_attr

from etools_datamart.apps.data.loader import EtoolsLoader
from etools_datamart.apps.etools.models import T2FTravel, T2FTravelactivity, T2FTravelattachment

from .base import EtoolsDataMartModel


class TravelAttachment(object):
    pass


class TripLoader(EtoolsLoader):
    def remove_deleted(self):
        country = self.context['country']
        # existing = list(self.get_queryset().only('id').values_list('id', flat=True))
        existing = list(T2FTravelactivity.objects.only('id').values_list('id', flat=True))
        to_delete = self.model.objects.filter(schema_name=country.schema_name).exclude(source_activity_id__in=existing)
        self.results.deleted += to_delete.count()
        to_delete.delete()

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for t2f_travel_activity in qs.all().order_by('id'):
            for travel in t2f_travel_activity.travels.all():
                travel.activity = t2f_travel_activity
                filters = self.config.key(self, travel)
                values = self.get_values(travel)
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def get_is_second_traveler(self, record: T2FTravel, values: dict, **kwargs):
        return record.traveler != record.activity.primary_traveler

    def get_attachments(self, record: T2FTravel, values: dict, **kwargs):
        return ",\n".join(list(map(lambda x: ":".join(x),
                                   record.attachments.values_list('type', 'file'))))

    def get_hact_visit_report(self, record: T2FTravel, values: dict, **kwargs):
        return "Yes" if T2FTravelattachment.objects.filter(
            travel=record,
            type__istartswith="HACT Programme Monitoring",
        ).exists() else ""

    def get_locations(self, record: T2FTravel, values: dict, **kwargs):
        # PartnersInterventionFlatLocations
        locs = []
        # intervention: PartnersIntervention = original.activity.intervention
        for location in record.activity.locations.select_related('gateway').order_by('id'):
            locs.append(dict(
                source_id=location.id,
                name=location.name,
                pcode=location.p_code,
                level=location.level,
                levelname=location.gateway.name
            ))
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def get_trip_attachments(self, record, values, **kwargs):
        return ",\n".join(list(map(lambda x: ":".join(x),
                                   record.attachments.values_list('type', 'file'))))


class ModeOfTravel:
    PLANE = 'Plane'
    BUS = 'Bus'
    CAR = 'Car'
    BOAT = 'Boat'
    RAIL = 'Rail'
    CHOICES = (
        (PLANE, 'Plane'),
        (BUS, 'Bus'),
        (CAR, 'Car'),
        (BOAT, 'Boat'),
        (RAIL, 'Rail')
    )


class Trip(EtoolsDataMartModel):
    PLANNED = 'planned'
    SUBMITTED = 'submitted'
    REJECTED = 'rejected'
    APPROVED = 'approved'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

    CHOICES = (
        (PLANNED, _('Planned')),
        (SUBMITTED, _('Submitted')),
        (REJECTED, _('Rejected')),
        (APPROVED, _('Approved')),
        (COMPLETED, _('Completed')),
        (CANCELLED, _('Cancelled')),
        (COMPLETED, _('Completed')),
    )
    additional_note = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    cancellation_note = models.TextField(blank=True, null=True)
    certification_note = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cp_output = models.TextField(blank=True, null=True)
    cp_output_id = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)
    estimated_travel_cost = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    hact_visit_report = models.CharField(max_length=300, blank=True, null=True)
    hidden = models.BooleanField(blank=True, null=True)
    international_travel = models.NullBooleanField(blank=True, null=True)
    is_driver = models.BooleanField(blank=True, null=True)
    is_second_traveler = models.CharField(max_length=300, blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True)
    misc_expenses = models.TextField(blank=True, null=True)
    mode_of_travel = ArrayField(models.CharField(max_length=5,
                                                 choices=ModeOfTravel.CHOICES),
                                null=True, blank=True, db_index=True,
                                verbose_name=_('Mode of Travel'))

    office_name = models.CharField(max_length=300, blank=True, null=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    pd_ssfa_reference_number = models.CharField(max_length=300, blank=True, null=True)
    pd_ssfa_title = models.CharField(max_length=300, blank=True, null=True)
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    primary_traveler = models.CharField(max_length=300, blank=True, null=True)
    purpose = models.CharField(max_length=500, blank=True, null=True)
    reference_number = models.CharField(max_length=12, blank=True, null=True, db_index=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejection_note = models.TextField(blank=True, null=True)
    report_note = models.TextField(blank=True, null=True)
    section_name = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=50,
                              choices=CHOICES,
                              blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    supervisor_email = models.CharField(max_length=300, blank=True, null=True)
    supervisor_name = models.CharField(max_length=300, blank=True, null=True)
    ta_required = models.NullBooleanField(blank=True, null=True)
    traveler_email = models.CharField(max_length=300, blank=True, null=True)
    traveler_name = models.CharField(max_length=300, blank=True, null=True)
    trip_attachments = models.TextField(blank=True, null=True)
    trip_activity_date = models.DateField(blank=True, null=True)
    trip_activity_type = models.CharField(max_length=300, blank=True, null=True)
    trip_activity_reference_number = models.CharField(max_length=300, blank=True, null=True)
    trip_url = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=300, blank=True, null=True)

    source_activity_id = models.IntegerField(blank=True, null=True)
    loader = TripLoader()

    class Meta:
        unique_together = ('schema_name', 'source_id', 'source_activity_id')

    class Options:
        source = T2FTravelactivity
        # last_modify_field = 'modified'
        key = lambda loader, travel: dict(schema_name=loader.context['country'].schema_name,
                                          source_id=travel.id,
                                          source_activity_id=travel.activity.id,
                                          )

        mapping = dict(
            cp_output="activity.result.name",
            cp_output_id="activity.result.vision_id",
            currency_code='currency.code',
            is_second_traveler="-",
            locations="-",
            locations_data="i",
            office_name="office.name",
            partner_name="activity.partner.name",
            pd_ssfa_reference_number='N/A',
            pd_ssfa_title='N/A',
            primary_traveler="activity.primary_traveler.email",
            section_name="section.name",
            supervisor_email='supervisor.email',
            supervisor_name=lambda loader, record: "%s %s" % (get_attr(record, 'supervisor.last_name'),
                                                              get_attr(record, 'supervisor.first_name')),
            traveler_email='traveler.email',
            traveler_name=lambda loader, record: "%s %s" % (record.traveler.last_name,
                                                            record.traveler.first_name),
            trip_attachments="-",
            trip_activity_date="activity.date",
            trip_activity_reference_number="activity.reference_number",
            trip_activity_type="activity.travel_type",
            trip_url=lambda loader, record: 't2f/edit-travel/%s' % record.id,
            vendor_number="activity.partner.vendor_number",
            source_activity_id='activity.id'
        )
