from django.db import models

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.mixins import LocationMixin
from etools_datamart.apps.etools.models import T2FTravel, T2FTravelactivity
from etools_datamart.apps.etools.patch import T2FTravel_CHOICES


class Travel(DataMartModel):
    additional_note = models.TextField(blank=True, null=True, )
    approved_at = models.DateTimeField(blank=True, null=True, db_index=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    cancellation_note = models.TextField(blank=True, null=True, )
    certification_note = models.TextField(blank=True, null=True, )
    completed_at = models.DateTimeField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(blank=True, null=True, db_index=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    # currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='publicscurrency_t2f_travel_currency_id', blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True, db_index=True)
    estimated_travel_cost = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=4)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    hidden = models.BooleanField(blank=True, null=True, )
    international_travel = models.NullBooleanField(blank=True, null=True, )
    is_driver = models.BooleanField(blank=True, null=True, )
    misc_expenses = models.TextField(blank=True, null=True, )
    mode_of_travel = models.TextField(blank=True, null=True)  # This field type is a guess.
    # office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='usersoffice_t2f_travel_office_id', blank=True, null=True)
    office_name = models.CharField(max_length=254, blank=True, null=True, db_index=True)
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    purpose = models.CharField(blank=True, null=True, max_length=500)
    reference_number = models.CharField(blank=True, null=True, max_length=12)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejection_note = models.TextField(blank=True, null=True, )
    report_note = models.TextField(blank=True, null=True, )
    # section = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name='reportssector_t2f_travel_section_id', blank=True, null=True)
    section_name = models.CharField(max_length=45, blank=True, null=True, db_index=True)
    start_date = models.DateTimeField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=50, choices=T2FTravel_CHOICES, db_index=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    # supervisor = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_t2f_travel_supervisor_id', blank=True, null=True)
    supervisor_email = models.CharField(max_length=200, blank=True, null=True)
    ta_required = models.NullBooleanField(blank=True, null=True, )
    # traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_t2f_travel_traveler_id', blank=True, null=True)
    traveler_email = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    class Meta:
        unique_together = ('schema_name', 'reference_number')

    class Options:
        # depends = (Intervention,)
        source = T2FTravel
        # queryset = lambda: FundsFundsreservationitem.objects.select_related('fund_reservation')
        # last_modify_field = 'modified'
        # key = lambda loader, record: dict(country_name=loader.context['country'].name,
        #                                   schema_name=loader.context['country'].schema_name,
        #                                   reference_number=record.reference_number)

        mapping = dict(office_name='office.name',
                       section_name='section.name',
                       supervisor_email='supervisor.email',
                       traveler_email='traveler.email',
                       currency_code='currency.code')


class TravelActivityLoader(Loader):

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for record in qs.order_by('id', '-date'):
            record.travel = record.travels.order_by('id').first()
            if record.travel:
                for location in record.locations.order_by('id'):
                    record.location = location
                    filters = self.config.key(self, record)
                    values = self.get_values(record)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)
            # else:
            #     # TODO: remove me
            #     print(111, "travel.py:85", record)


class TravelActivity(LocationMixin, DataMartModel):
    travel_reference_number = models.CharField(max_length=200, blank=True, null=True)
    travel_type = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    partner_name = models.CharField(max_length=200, blank=True, null=True)
    partnership_number = models.CharField(max_length=200, blank=True, null=True)
    primary_traveler = models.CharField(max_length=200, blank=True, null=True)

    # internal
    source_travel_id = models.IntegerField(null=True)
    source_partner_id = models.IntegerField(null=True)
    source_partnership_id = models.IntegerField(null=True)

    loader = TravelActivityLoader()

    class Meta:
        unique_together = ('schema_name',
                           'source_id',
                           'travel_reference_number',
                           'location_source_id')

    class Options:
        depends = (Travel,)
        source = T2FTravelactivity
        last_modify_field = None
        key = lambda loader, record: dict(country_name=loader.context['country'].name,
                                          schema_name=loader.context['country'].schema_name,
                                          source_id=record.id,
                                          location_source_id=record.location.id,
                                          )
        mapping = {
            'source_travel_id': 'travel.id',
            'source_partner_id': 'partner.id',
            'source_partnership_id': 'partnership.id',
            'location_source_id': 'location.id',
            'location_name': 'location.name',
            'location_pcode': 'location.p_code',
            'location_level': 'location.level',
            'location_levelname': 'location.gateway.name',
            'travel_reference_number': 'travel.reference_number',
            'primary_traveler': 'primary_traveler.email',
            'partner_name': 'partner.name',
            'partnership_number': 'partnership.number'
        }
