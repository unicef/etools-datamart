from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.models import FundsFundsreservationheader

from .base import EtoolsDataMartModel
from .intervention import Intervention


class FundsReservationHeader(EtoolsDataMartModel):
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
    created = models.DateTimeField()
    modified = models.DateTimeField()
    actual_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    multi_curr_flag = models.BooleanField()
    completed_flag = models.BooleanField(default=None, blank=True, null=True)
    delegated = models.BooleanField(default=None, blank=True, null=True)
    pd_reference_number = models.CharField(max_length=256, blank=True, null=True)

    loader = EtoolsLoader()

    class Meta:
        unique_together = (("fr_number", "vendor_code"),)

    class Options:
        depends = (Intervention,)
        source = FundsFundsreservationheader
        queryset = lambda: FundsFundsreservationheader.objects.select_related("intervention")
        last_modify_field = "modified"

        mapping = dict(
            pd_reference_number="intervention.reference_number",
        )
