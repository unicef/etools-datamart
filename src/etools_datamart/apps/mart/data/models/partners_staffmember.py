# -*- coding: utf-8 -*-
# import django_filters
from django.db import models

from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import PartnersPartnerstaffmember


class PartnerStaffMember(EtoolsDataMartModel):
    title = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    vendor_number = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Options:
        source = PartnersPartnerstaffmember
        mapping = {'partner': 'partner.name',
                   'vendor_number': 'partner.vendor_number'}
