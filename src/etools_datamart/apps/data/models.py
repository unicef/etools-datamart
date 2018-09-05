# -*- coding: utf-8 -*-
import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

logger = logging.getLogger(__name__)


class DataMartManager(models.Manager):
    def truncate(self):
        self.raw('TRUNCATE TABLE {0}'.format(self.model._meta.db_table))


class DataMartModel(models.Model):
    class Meta:
        abstract = True

    objects = DataMartManager()

    # @classproperty
    # def task_log(cls):
    #     from etools_datamart.apps.etl.models import TaskLog
    #     return TaskLog.objects.get_or_create(task=cls._etl_loader,
    #                                          defaults=dict(content_type=ContentType.objects.get_for_model(cls),
    #                                                        timestamp=None,
    #                                                        table_name=cls._meta.db_table))[0]


class PMPIndicators(DataMartModel):
    country_name = models.CharField(max_length=50, null=True, db_index=True)
    vendor_number = models.CharField(max_length=255, null=True, db_index=True)
    business_area_code = models.CharField(max_length=100, null=True, db_index=True)

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


class Intervention(DataMartModel):
    country_name = models.CharField(max_length=50, null=True, db_index=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(null=True)
    document_type = models.CharField(max_length=255, null=True)
    number = models.CharField(max_length=64, null=True)
    title = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=32, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    submission_date = models.DateField(null=True)
    submission_date_prc = models.DateField(null=True)
    review_date_prc = models.DateField(null=True)
    prc_review_document = models.CharField(max_length=1024, null=True)
    signed_by_unicef_date = models.DateField(null=True)
    signed_by_partner_date = models.DateField(null=True)
    population_focus = models.CharField(max_length=130, null=True)
    partner_authorized_officer_signatory_id = models.IntegerField(null=True)
    signed_pd_document = models.CharField(max_length=1024, null=True)
    contingency_pd = models.NullBooleanField(null=True)
    metadata = JSONField()

    unicef_signatory_first_name = models.CharField(max_length=30, null=True)
    unicef_signatory_last_name = models.CharField(max_length=30, null=True)
    unicef_signatory_email = models.CharField(max_length=254, null=True)

    partner_signatory_title = models.CharField(max_length=64, null=True)
    partner_signatory_first_name = models.CharField(max_length=64, null=True)
    partner_signatory_last_name = models.CharField(max_length=64, null=True)
    partner_signatory_email = models.CharField(max_length=128, null=True)
    partner_signatory_phone = models.CharField(max_length=64, null=True)

    unicef_focal_point_first_name = models.CharField(max_length=30, null=True)
    unicef_focal_point_last_name = models.CharField(max_length=30, null=True)
    unicef_focal_point_email = models.CharField(max_length=254, null=True)

    partner_focal_point_title = models.CharField(max_length=64, null=True)
    partner_focal_point_first_name = models.CharField(max_length=64, null=True)
    partner_focal_point_last_name = models.CharField(max_length=64, null=True)
    partner_focal_point_email = models.CharField(max_length=128, null=True)
    partner_focal_point_phone = models.CharField(max_length=64, null=True)

    intervention_id = models.IntegerField(null=True)
    agreement_id = models.IntegerField(null=True)
    country_programme_id = models.IntegerField(null=True)
    unicef_signatory_id = models.IntegerField(null=True)
