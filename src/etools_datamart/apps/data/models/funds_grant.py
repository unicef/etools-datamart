from django.db import models

from etools_datamart.apps.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.etools.models import FundsGrant


class Grant(EtoolsDataMartModel):
    name = models.CharField(max_length=128, blank=True, null=True)
    donor = models.CharField(max_length=128, blank=True, null=True)
    expiry = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Options:
        source = FundsGrant
        mapping = dict(donor='donor.name')
