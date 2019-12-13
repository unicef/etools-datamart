from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.models import FundsFundsreservationitem

from .base import EtoolsDataMartModel
from .intervention import Intervention


class FundsReservationLoader(EtoolsLoader):
    def get_intervention(self, record, values, **kwargs):
        if record.fund_reservation.intervention:
            try:
                return Intervention.objects.get(
                    schema_name=self.context['country'].schema_name,
                    source_id=record.fund_reservation.intervention.pk)
            except Intervention.DoesNotExist:
                pass


class FundsReservation(EtoolsDataMartModel):
    # header
    vendor_code = models.CharField(max_length=20)
    fr_number = models.CharField(max_length=20)
    document_date = models.DateField(blank=True, null=True)
    fr_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    document_text = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    actual_amt = models.DecimalField(max_digits=20, decimal_places=2)
    intervention_amt = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt = models.DecimalField(max_digits=20, decimal_places=2)
    # created = models.DateTimeField()
    # modified = models.DateTimeField()
    actual_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_local = models.DecimalField(max_digits=20, decimal_places=2,
                                          blank=True, null=True)
    multi_curr_flag = models.BooleanField()
    completed_flag = models.BooleanField(default=None, blank=True, null=True)
    delegated = models.BooleanField(default=None, blank=True, null=True)

    # item
    fr_ref_number = models.CharField(max_length=30)
    line_item = models.SmallIntegerField()
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    overall_amount = models.DecimalField(max_digits=20, decimal_places=2)
    overall_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    line_item_text = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    donor = models.CharField(max_length=256, blank=True, null=True)
    donor_code = models.CharField(max_length=30, blank=True, null=True)
    intervention_title = models.CharField(max_length=256, blank=True, null=True)

    # extras
    pd_ssfa_number = models.CharField(max_length=64, null=True)

    # internals
    source_id = models.IntegerField()
    source_intervention_id = models.IntegerField()
    intervention = models.ForeignKey(Intervention,
                                     models.SET_NULL,
                                     related_name='funds', blank=True, null=True)

    loader = FundsReservationLoader()

    class Meta:
        unique_together = (('schema_name', 'source_id'),)
        verbose_name = "Funds Reservation"

    class Options:
        depends = (Intervention,)
        source = FundsFundsreservationitem
        queryset = lambda: FundsFundsreservationitem.objects.select_related('fund_reservation')
        last_modify_field = 'modified'
        # key = lambda loader, record: dict(country_name=loader.context['country'].name,
        #                                   schema_name=loader.context['country'].schema_name,
        #                                   fr_number=record.fund_reservation.fr_number)

        mapping = dict(
            vendor_code='fund_reservation.vendor_code',
            fr_number='fund_reservation.fr_number',
            document_date='fund_reservation.document_date',
            pd_ssfa_number='fund_reservation.number',
            fr_type='fund_reservation.fr_type',
            currency='fund_reservation.currency',

            document_text='fund_reservation.document_text',
            start_date='fund_reservation.start_date',
            end_date='fund_reservation.end_date',
            actual_amt='fund_reservation.actual_amt',
            intervention_amt='fund_reservation.intervention_amt',
            outstanding_amt='fund_reservation.outstanding_amt',
            total_amt='fund_reservation.total_amt',
            actual_amt_local='fund_reservation.actual_amt_local',
            total_amt_local="fund_reservation.total_amt_local",
            outstanding_amt_local='fund_reservation.outstanding_amt_local',
            multi_curr_flag='fund_reservation.multi_curr_flag',
            completed_flag='fund_reservation.completed_flag',
            intervention_title="fund_reservation.intervention.title",
            # delegated="fund_reservation.intervention.delegated",
            delegated='i',
            source_id='id',
            source_intervention_id='fund_reservation.id',
            seen="=",
            country_name="=",
            schema_name="=",
            area_code="=",
            fr_ref_number="=",
            line_item="=",
            wbs="wbs",
            grant_number="=",
            fund="fund",
            overall_amount="=",
            overall_amount_dc="=",
            due_date="=",
            line_item_text="=",
            created="=",
            modified="=",
            donor="=",
            donor_code="=",
        )
