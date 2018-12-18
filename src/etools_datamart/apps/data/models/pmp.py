# -*- coding: utf-8 -*-
import logging

from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel

logger = logging.getLogger(__name__)


class PMPIndicators(DataMartModel):
    vendor_number = models.CharField(max_length=255, null=True, db_index=True)

    partner_name = models.CharField(max_length=255, null=True, db_index=True)
    partner_type = models.CharField(max_length=255, null=True, db_index=True)
    pd_ssfa_ref = models.CharField(max_length=255, null=True)
    pd_ssfa_status = models.CharField(max_length=50, null=True, db_index=True)
    pd_ssfa_start_date = models.DateField(null=True, )
    pd_ssfa_creation_date = models.DateField(null=True, )
    pd_ssfa_end_date = models.DateField(null=True, )

    cash_contribution = models.DecimalField(max_digits=20, decimal_places=3,
                                            null=True, help_text='UNICEF US$ Cash contribution')
    supply_contribution = models.DecimalField(max_digits=20, decimal_places=3,
                                              null=True, help_text='UNICEF US$ Supply contribution')
    total_budget = models.DecimalField(max_digits=20, decimal_places=3, null=True, db_index=True,
                                       help_text='Total Budget')
    unicef_budget = models.DecimalField(max_digits=20, decimal_places=3, null=True, help_text='UNICEF Budget')

    currency = models.CharField(max_length=201, null=True, help_text='Currency')
    partner_contribution = models.CharField(max_length=202, null=True, help_text='Partner Contribution')
    unicef_cash = models.CharField(max_length=203, null=True, help_text='Unicef Cash')
    in_kind_amount = models.CharField(max_length=204, null=True, help_text='In kind Amount')
    total = models.CharField(max_length=205, null=True, help_text='')
    fr_numbers_against_pd_ssfa = models.TextField(null=True, help_text='FR numbers against PD / SSFA')
    fr_currencies = models.CharField(max_length=207, null=True, help_text='FR currencies')
    sum_of_all_fr_planned_amount = models.CharField(max_length=208, null=True, help_text='Sum of all FR planned amount')
    core_value_attached = models.CharField(max_length=209, null=True, help_text='Core value attached')
    partner_link = models.CharField(max_length=210, null=True, help_text='Partner Link')
    intervention_link = models.CharField(max_length=211, null=True, help_text='Intervention Link')

    country_id = models.IntegerField(null=True)
    partner_id = models.IntegerField(null=True)
    intervention_id = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(null=True)

    class Meta:
        ordering = ('country_name', 'partner_name')
        verbose_name = "PMP Indicator"
