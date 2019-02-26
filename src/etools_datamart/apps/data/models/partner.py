from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import PartnersPartnerorganization
from etools_datamart.apps.etools.patch import PartnerOrganization, PartnerType


class Partner(DataMartModel):
    address = models.TextField(blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    basis_for_risk_rating = models.CharField(max_length=50, blank=True, null=True)
    blocked = models.BooleanField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    core_values_assessment_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    cso_type = models.CharField(max_length=50, blank=True, null=True,
                                db_index=True,
                                choices=PartnerOrganization.CSO_TYPES)
    deleted_flag = models.BooleanField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    hact_values = models.TextField(blank=True, null=True)  # This field type is a guess.
    hidden = models.BooleanField(db_index=True, blank=True, null=True)
    last_assessment_date = models.DateField(blank=True, null=True)
    manually_blocked = models.BooleanField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    net_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    outstanding_dct_amount_6_to_9_months_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True,
                                                                   null=True)
    outstanding_dct_amount_more_than_9_months_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True,
                                                                        null=True)
    partner_type = models.CharField(max_length=50, db_index=True,
                                    blank=True, null=True,
                                    choices=PartnerType.CHOICES)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    postal_code = models.CharField(max_length=32, blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True,
                              db_index=True,
                              choices=PartnerOrganization.RISK_RATINGS)
    reported_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    shared_with = ArrayField(
        models.CharField(max_length=20, blank=True, choices=PartnerOrganization.AGENCY_CHOICES),
        verbose_name=_("Shared Partner"),
        blank=True,
        null=True
    )
    short_name = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=500, blank=True, null=True)
    total_ct_cp = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_ytd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    type_of_assessment = models.CharField(max_length=50, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True, db_index=True, )
    vision_synced = models.BooleanField(blank=True, null=True)

    class Meta:
        unique_together = (('schema_name', 'name', 'vendor_number'),
                           ('schema_name', 'vendor_number'),)

    class Options:
        source = PartnersPartnerorganization
        key = lambda loader, record: dict(country_name=loader.context['country'].name,
                                          schema_name=loader.context['country'].schema_name,
                                          source_id=record.id)
