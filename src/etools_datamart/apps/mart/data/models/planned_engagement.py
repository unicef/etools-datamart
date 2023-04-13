from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Partner
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from django.db import models

from etools_datamart.apps.sources.etools.models import PartnersPlannedengagement


class PartnersPlannedEngagement(EtoolsDataMartModel):
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    spot_check_planned_q1 = models.IntegerField(blank=True, null=True)
    spot_check_planned_q2 = models.IntegerField(blank=True, null=True)
    spot_check_planned_q3 = models.IntegerField(blank=True, null=True)
    spot_check_planned_q4 = models.IntegerField(blank=True, null=True)
    scheduled_audit = models.BooleanField(blank=True, null=True)
    special_audit = models.BooleanField(blank=True, null=True)
    spot_check_follow_up = models.IntegerField(blank=True, null=True)

    loader = EtoolsLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = PartnersPlannedengagement
        depends = (Partner,)
        mapping = dict(
            partner_name='partner.name',
            type='partner.cso_type',
            vendor_number='partner.vendor_number',
        )
