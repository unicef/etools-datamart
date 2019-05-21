# -*- coding: utf-8 -*-
import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.report_sector import Section
from etools_datamart.apps.etools.models import PartnersIntervention

from .base import DataMartModel
from .location import Location
from .mixins import add_location_mapping, LocationMixin
from .partner import Partner
from .user_office import Office

logger = logging.getLogger(__name__)



class InterventionLoader(Loader):
    # def fr_currencies_ok(self, original: PartnersIntervention):
    #     return original.frs__currency__count == 1 if original.frs__currency__count else None

    def get_sections(self, original: PartnersIntervention, values: dict):
        # PartnersInterventionFlatLocations
        ids = list(original.sections.values_list("id", flat=True))
        ret = list(Section.objects.filter(source_id__in=ids,
                                          schema_name=values['schema_name']).values("id",
                                                                                    "name",
                                                                                    "source_id",
                                                                                    "description"))
        # assert len(ids) == len(ret)
        return ret

    def get_locations(self, original: PartnersIntervention, values: dict):
        # PartnersInterventionFlatLocations
        ids = list(original.flat_locations.values_list("id", flat=True))
        ret = list(Location.objects.filter(source_id__in=ids,
                                           schema_name=values['schema_name']).values("id",
                                                                                     "name",
                                                                                     "source_id",
                                                                                     "p_code"))
        # assert len(ids) == len(ret)
        return ret

    def get_offices(self, original: PartnersIntervention, values: dict):
        # PartnersInterventionOffices
        ids = list(original.offices.values_list("id", flat=True))
        ret = list(Office.objects.filter(source_id__in=ids,
                                         schema_name=values['schema_name']).values("id",
                                                                                   "name",
                                                                                   "source_id",
                                                                                   "zonal_chief_email",
                                                                                   "zonal_chief_source_id"))
        # assert len(ids) == len(ret)
        return ret

    # def get_disbursement_percent(self, original: PartnersIntervention, values: dict):
    #     if original.frs__actual_amt_local__sum is None:
    #         return None
    #
    #     if not (self.fr_currencies_ok(original) and original.max_fr_currency == original.planned_budget.currency):
    #         return "!Error! (currencies do not match)"
    #     percent = original.frs__actual_amt_local__sum / original.total_unicef_cash * 100 \
    #         if original.total_unicef_cash and original.total_unicef_cash > 0 else 0
    #     return "%.1f" % percent


class InterventionAbstract(models.Model):
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

    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=4, blank=True, null=True)

    intervention_id = models.IntegerField(blank=True, null=True)
    agreement_id = models.IntegerField(blank=True, null=True)
    country_programme_id = models.IntegerField(blank=True, null=True)
    unicef_signatory_id = models.IntegerField(blank=True, null=True)

    offices = JSONField(blank=True, null=True, default=dict)
    locations = JSONField(blank=True, null=True, default=dict)
    sections = JSONField(blank=True, null=True, default=dict)

    partner_id = models.IntegerField(blank=True, null=True)
    partner_source_id = models.IntegerField(blank=True, null=True)

    # disbursement_percent = models.IntegerField('Disbursement To Date (%)')

    class Meta:
        abstract = True

    class Options:
        depends = (Office, Location, Partner)
        source = PartnersIntervention
        queryset = lambda: PartnersIntervention.objects.select_related('agreement',
                                                                       'partner_authorized_officer_signatory',
                                                                       'unicef_signatory',
                                                                       'country_programme',
                                                                       'partnersintervention_partners_interventionbudget_intervention_id'
                                                                       )
        key = lambda loader, record: dict(country_name=loader.context['country'].name,
                                          schema_name=loader.context['country'].schema_name,
                                          area_code=loader.context['country'].business_area_code,
                                          intervention_id=record.pk)
        mapping = dict(start_date='start',
                       end_date='end',
                       partner_name='agreement.partner.name',
                       partner_source_id='agreement.partner.id',
                       partner_id=lambda loader, record: Partner.objects.get(source_id=record.agreement.partner.id,
                                                                             country_name=loader.context['country']).id,
                       partner_authorized_officer_signatory_id='partner_authorized_officer_signatory.pk',
                       country_programme_id='country_programme.pk',
                       intervention_id='id',
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
                       updated='modified',

                       partner_contribution='planned_budget.partner_contribution',
                       unicef_cash='planned_budget.unicef_cash',
                       in_kind_amount='planned_budget.in_kind_amount',
                       partner_contribution_local='planned_budget.partner_contribution_local',
                       unicef_cash_local='planned_budget.unicef_cash_local',
                       in_kind_amount_local='planned_budget.in_kind_amount_local',
                       total='planned_budget.total',
                       total_local='planned_budget.total_local',
                       currency='planned_budget.currency',
                       )


class Intervention(InterventionAbstract, DataMartModel):
    loader = InterventionLoader()

    class Meta:
        ordering = ('country_name', 'title')
        verbose_name = "Intervention"
        unique_together = ('schema_name', 'intervention_id')

    class Options(InterventionAbstract.Options):
        pass


class InterventionByLocationLoader(InterventionLoader):
    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for intervention in qs.all():
            for location in intervention.flat_locations.all().order_by('id'):
                intervention.location = location
                filters = self.config.key(self, intervention)
                values = self.get_values(intervention)
                op = self.process_record(filters, values)
                self.increment_counter(op)


class InterventionByLocation(LocationMixin, InterventionAbstract, DataMartModel):
    loader = InterventionByLocationLoader()

    class Meta:
        ordering = ('country_name', 'title')
        verbose_name = "Intervention By Location"
        unique_together = ('schema_name', 'intervention_id', 'location_source_id')

    class Options(InterventionAbstract.Options):
        key = lambda loader, record: dict(country_name=loader.context['country'].name,
                                          schema_name=loader.context['country'].schema_name,
                                          area_code=loader.context['country'].business_area_code,
                                          intervention_id=record.pk,
                                          location_source_id=record.location.pk)
        mapping = add_location_mapping(InterventionAbstract.Options.mapping)
