from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.enrichment.consts import T2FTravelConsts
from etools_datamart.apps.sources.etools.models import T2FTravel

from .base import EtoolsDataMartModel


class TravelLoader(EtoolsLoader):
    def get_attachments(self, record, values, **kwargs):
        return ",\n".join(
            list(map(lambda x: ":".join(x), record.T2FTravelattachment_travel.values_list("type", "file")))
        )


class Travel(EtoolsDataMartModel):
    additional_note = models.TextField(
        blank=True,
        null=True,
    )
    approved_at = models.DateTimeField(blank=True, null=True, db_index=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    cancellation_note = models.TextField(
        blank=True,
        null=True,
    )
    certification_note = models.TextField(
        blank=True,
        null=True,
    )
    completed_at = models.DateTimeField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(blank=True, null=True, db_index=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    # currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='publicscurrency_t2f_travel_currency_id', blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)
    estimated_travel_cost = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=4)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    hidden = models.BooleanField(
        blank=True,
        null=True,
    )
    international_travel = models.BooleanField(
        blank=True,
        null=True,
    )
    is_driver = models.BooleanField(
        blank=True,
        null=True,
    )
    misc_expenses = models.TextField(
        blank=True,
        null=True,
    )
    mode_of_travel = models.TextField(blank=True, null=True)  # This field type is a guess.
    # office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='usersoffice_t2f_travel_office_id', blank=True, null=True)
    office_name = models.CharField(max_length=254, blank=True, null=True, db_index=True)
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    purpose = models.CharField(blank=True, null=True, max_length=500)
    reference_number = models.CharField(blank=True, null=True, max_length=12)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejection_note = models.TextField(
        blank=True,
        null=True,
    )
    report_note = models.TextField(
        blank=True,
        null=True,
    )
    # section = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name='reportssector_t2f_travel_section_id', blank=True, null=True)
    section_name = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=50, choices=T2FTravelConsts.CHOICES, db_index=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    # supervisor = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_t2f_travel_supervisor_id', blank=True, null=True)
    supervisor_email = models.CharField(max_length=200, blank=True, null=True)
    ta_required = models.BooleanField(
        blank=True,
        null=True,
    )
    # traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_t2f_travel_traveler_id', blank=True, null=True)
    traveler_email = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    attachments = models.TextField(blank=True, null=True)

    loader = TravelLoader()

    class Meta:
        unique_together = ("schema_name", "reference_number")

    class Options:
        # depends = (Intervention,)
        source = T2FTravel
        # queryset = lambda: FundsFundsreservationitem.objects.select_related('fund_reservation')
        # last_modify_field = 'modified'
        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name, reference_number=record.reference_number
        )

        mapping = dict(
            office_name="office.name",
            section_name="section.name",
            supervisor_email="supervisor.email",
            traveler_email="traveler.email",
            currency_code="currency.code",
        )
