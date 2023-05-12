from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.models import FundsFundsreservationitem

from . import FundsReservation, FundsReservationHeader
from .base import EtoolsDataMartModel


class FundsReservationItem(EtoolsDataMartModel):
    fund_reservation_number = models.CharField(max_length=20)

    fr_ref_number = models.CharField(max_length=30)
    line_item = models.SmallIntegerField()
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    overall_amount = models.DecimalField(max_digits=20, decimal_places=2)
    overall_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    line_item_text = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    donor = models.CharField(max_length=256, blank=True, null=True)
    donor_code = models.CharField(max_length=30, blank=True, null=True)

    loader = EtoolsLoader()

    class Meta:
        unique_together = (("fund_reservation_number", "line_item"),)

    class Options:
        depends = (FundsReservationHeader,)
        source = FundsFundsreservationitem
        queryset = lambda: FundsFundsreservationitem.objects.select_related("fund_reservation")
        last_modify_field = "modified"

        mapping = dict(
            fund_reservation_number="fund_reservation.fr_number",
        )
