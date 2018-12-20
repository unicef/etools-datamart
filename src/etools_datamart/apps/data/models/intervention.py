# -*- coding: utf-8 -*-
import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import PartnersIntervention

logger = logging.getLogger(__name__)


class Intervention(DataMartModel):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(null=True)
    document_type = models.CharField(max_length=255, null=True)
    number = models.CharField(max_length=64, null=True)
    title = models.CharField(max_length=256, null=True, db_index=True)
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

    partner_name = models.CharField(max_length=200, null=True)
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

    class Meta:
        ordering = ('country_name', 'title')
        verbose_name = "Intervention"

    class Options:
        source = PartnersIntervention
        queryset = lambda: PartnersIntervention.objects.select_related('agreement',
                                                                       'partner_authorized_officer_signatory',
                                                                       'unicef_signatory',
                                                                       'country_programme',
                                                                       )
        key = lambda country, record: dict(country_name=country.name,
                                           schema_name=country.schema_name,
                                           area_code=country.business_area_code,
                                           intervention_id=record.pk)
        mapping = dict(start_date='start',
                       end_date='end',
                       partner_name='agreement.partner.name',
                       partner_authorized_officer_signatory_id='partner_authorized_officer_signatory.pk',
                       country_programme_id='country_programme.pk',
                       intervention_id='pk',
                       unicef_signatory_id='unicef_signatory.pk',
                       unicef_signatory_first_name='unicef_signatory.first_name',
                       unicef_signatory_last_name='unicef_signatory.last_name',
                       unicef_signatory_email='unicef_signatory.email',

                       partner_signatory_title='partner_authorized_officer_signatory.title',
                       partner_signatory_first_name='partner_authorized_officer_signatory.first_name',
                       partner_signatory_last_name='partner_authorized_officer_signatory.last_name',
                       partner_signatory_email='partner_authorized_officer_signatory.email',
                       partner_signatory_phone='partner_authorized_officer_signatory.phone',
                       partner_focal_point_title='partner_focal_point.title',
                       partner_focal_point_first_name='partner_focal_point.first_name',
                       partner_focal_point_last_name='partner_focal_point.last_name',
                       partner_focal_point_email='partner_focal_point.email',
                       partner_focal_point_phone='partner_focal_point.phone',
                       updated='modified')
