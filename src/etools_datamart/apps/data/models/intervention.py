# -*- coding: utf-8 -*-
import logging

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import F

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.report_sector import Section
from etools_datamart.apps.etools.models import (PartnersAgreementamendment, PartnersIntervention,
                                                PartnersInterventionplannedvisits,
                                                ReportsAppliedindicator, ReportsLowerresult, )

from .base import DataMartModel
from .location import Location
from .mixins import add_location_mapping, LocationMixin
from .partner import Partner
from .user_office import Office

logger = logging.getLogger(__name__)


class InterventionLoader(Loader):
    # def fr_currencies_ok(self, original: PartnersIntervention):
    #     return original.frs__currency__count == 1 if original.frs__currency__count else None

    def get_planned_programmatic_visits(self, original: PartnersIntervention, values: dict):
        qs = PartnersInterventionplannedvisits.objects.filter(intervention=original)
        qs = qs.filter(year=self.context['today'].year)
        qs = qs.annotate(
            planned=F('programmatic_q1') + F('programmatic_q2') + F('programmatic_q3') + F('programmatic_q4'))
        record = qs.first()
        if record:
            return record.planned

    def get_attachment_types(self, original: PartnersIntervention, values: dict):
        qs = original.attachments.all()
        values['number_of_attachments'] = qs.count()
        return ", ".join(qs.values_list('type__name', flat=True))

    def get_amendment_types(self, original: PartnersIntervention, values: dict):
        qs = PartnersAgreementamendment.objects.filter(agreement=original.agreement).order_by('signed_date')
        values['number_of_amendments'] = qs.count()
        if qs:
            values['last_amendment_date'] = qs.latest('signed_date').signed_date
        types = [str(t) for t in qs.values_list('types', flat=True)]
        return ", ".join(types)

    def get_days_from_prc_review_to_signature(self, original: PartnersIntervention, values: dict):
        i1 = original.review_date_prc
        i2 = original.signed_by_partner_date
        if i1 and i2:
            return (i2 - i1).days

    def get_days_from_submission_to_signature(self, original: PartnersIntervention, values: dict):
        i1 = original.submission_date
        i2 = original.signed_by_unicef_date
        if i1 and i2:
            return (i2 - i1).days

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
        locs = []
        for location in original.flat_locations.select_related('gateway').order_by('id'):
            locs.append(dict(
                source_id=location.id,
                name=location.name,
                pcode=location.p_code,
                level=location.level,
                levelname=location.gateway.name
            ))
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def get_offices(self, original: PartnersIntervention, values: dict):
        # PartnersInterventionOffices
        data = []
        for office in original.offices.select_related('zonal_chief').order_by('id'):
            data.append(dict(source_id=office.id,
                             name=office.name,
                             zonal_chief_email=getattr(office.zonal_chief, 'email', ''),
                             ))
        # ids = list(original.offices.values_list("id", flat=True))
        # ret = list(Office.objects.filter(source_id__in=ids,
        #                                  schema_name=values['schema_name']).values("id",
        #                                                                            "name",
        #                                                                            "source_id",
        #                                                                            "zonal_chief_email",
        #                                                                            "zonal_chief_source_id"))
        # values['offices_data'] = {}
        # assert len(ids) == len(ret)
        values['offices_data'] = data
        return ", ".join([l['name'] for l in data])

    def get_clusters(self, original: PartnersIntervention, values: dict):
        qs = ReportsLowerresult.objects.filter(result_link__intervention=original)
        # qs = PartnersInterventionresultlink.objects.filter(intervention=original)
        # for lower_result in qs.all():
        # all_lower_results = [lower_result for link in original.result_links.all()
        #                      for lower_result in link.ll_results.all()
        #                      ]

        qs = ReportsAppliedindicator.objects.filter(lower_result__result_link__intervention=original)
        clusters = set()
        for applied_indicator in qs.all():
            if applied_indicator.cluster_name:
                clusters.add(applied_indicator.cluster_name)
        return clusters

    def get_partner_focal_points(self, original: PartnersIntervention, values: dict):
        data = []
        ret = []
        for member in original.partner_focal_points.all():
            # member is PartnersPartnerstaffmember
            ret.append("{0.last_name} {0.first_name} ({0.email}) {0.phone}".format(member))
            data.append(dict(last_name=member.last_name,
                         first_name=member.first_name,
                         email=member.email,
                         phone=member.phone,
                         ))

        values['partner_focal_points_data'] = data
        return ", ".join(ret)

    def get_unicef_focal_points(self, original: PartnersIntervention, values: dict):
        # ret = []
        # for member in original.unicef_focal_points.all():
        #     # member is PartnersPartnerstaffmember
        #     ret.append("{0.last_name} {0.first_name} {0.email}".format(member))
        # values['unicef_focal_points_data'] = {}
        # return "\n".join(ret)
        data = []
        ret = []
        for member in original.unicef_focal_points.all():
            # member is PartnersPartnerstaffmember
            ret.append("{0.last_name} {0.first_name} ({0.email})".format(member))
            data.append(dict(last_name=member.last_name,
                         first_name=member.first_name,
                         email=member.email,
                         ))

        values['unicef_focal_points_data'] = data
        return ", ".join(ret)


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
    agreement_reference_number = models.CharField(max_length=300, blank=True, null=True)
    amendment_types = models.TextField(blank=True, null=True)
    attachment_types = models.TextField(blank=True, null=True)
    agreement_id = models.IntegerField(blank=True, null=True)
    clusters = models.TextField(blank=True, null=True)
    contingency_pd = models.NullBooleanField(null=True)
    cp_output = models.CharField(max_length=300, blank=True, null=True)
    cp_output_id = models.IntegerField(blank=True, null=True)
    cso_type = models.CharField(max_length=300, blank=True, null=True)
    country_programme = models.CharField(max_length=300, blank=True, null=True)
    country_programme_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=4, blank=True, null=True)
    days_from_prc_review_to_signature = models.IntegerField(blank=True, null=True)
    days_from_submission_to_signature = models.IntegerField(blank=True, null=True)
    document_type = models.CharField(max_length=255, null=True)
    end_date = models.DateField(null=True)
    fr_number = models.CharField(max_length=300, blank=True, null=True)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    intervention_id = models.IntegerField(blank=True, null=True)
    last_amendment_date = models.DateField(blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)
    metadata = JSONField()
    number = models.CharField(max_length=64, null=True)
    number_of_attachments = models.IntegerField(blank=True, null=True)
    number_of_amendments = models.IntegerField(blank=True, null=True)
    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)
    partner_authorized_officer_signatory_id = models.IntegerField(null=True)
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_focal_points = models.TextField(blank=True, null=True)
    partner_focal_points_data = JSONField(blank=True, null=True, default=dict)
    # partner_focal_point_email = models.CharField(max_length=128, null=True)
    # partner_focal_point_first_name = models.CharField(max_length=64, null=True)
    # partner_focal_point_last_name = models.CharField(max_length=64, null=True)
    # partner_focal_point_phone = models.CharField(max_length=64, null=True)
    # partner_focal_point_title = models.CharField(max_length=64, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=200, null=True)
    partner_signatory_email = models.CharField(max_length=128, null=True)
    partner_signatory_first_name = models.CharField(max_length=64, null=True)
    partner_signatory_last_name = models.CharField(max_length=64, null=True)
    partner_signatory_phone = models.CharField(max_length=64, null=True)
    partner_signatory_title = models.CharField(max_length=64, null=True)
    partner_source_id = models.IntegerField(blank=True, null=True)
    partner_type = models.CharField(max_length=64, null=True)
    partner_vendor_number = models.CharField(max_length=100, blank=True, null=True)
    planned_programmatic_visits = models.IntegerField(blank=True, null=True)
    population_focus = models.CharField(max_length=130, null=True)
    prc_review_document = models.CharField(max_length=1024, null=True)
    review_date_prc = models.DateField(null=True)
    sections = JSONField(blank=True, null=True, default=dict)
    signed_by_partner_date = models.DateField(null=True)
    signed_by_unicef_date = models.DateField(null=True)
    signed_pd_document = models.CharField(max_length=1024, null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=32, null=True)
    submission_date = models.DateField(null=True)
    submission_date_prc = models.DateField(null=True)
    title = models.CharField(max_length=256, null=True, db_index=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_focal_points = models.TextField(blank=True, null=True)
    unicef_focal_points_data = JSONField(blank=True, null=True, default=dict)

    unicef_signatory_email = models.CharField(max_length=254, null=True)
    unicef_signatory_first_name = models.CharField(max_length=30, null=True)
    unicef_signatory_id = models.IntegerField(blank=True, null=True)
    unicef_signatory_last_name = models.CharField(max_length=30, null=True)
    updated = models.DateTimeField(null=True)

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
        mapping = dict(
            agreement_reference_number='agreement.reference_number',
            amendment_types='-',
            attachment_types='-',
            clusters='-',
            contingency_pd='=',
            country_programme='country_programme.name',
            country_programme_id='country_programme.pk',
            cp_output_id=None,
            cp_output=None,
            created='=',
            cso_type=None,
            currency='planned_budget.currency',
            days_from_submission_to_signature='-',
            days_from_prc_review_to_signature='-',
            end_date='end',
            fr_number=None,
            in_kind_amount='planned_budget.in_kind_amount',
            in_kind_amount_local='planned_budget.in_kind_amount_local',
            intervention_id='id',
            last_amendment_date='i',
            locations_data='i',
            locations='-',
            number_of_amendments='i',
            number_of_attachments='i',
            offices='-',
            offices_data='i',
            partner_authorized_officer_signatory_id='partner_authorized_officer_signatory.pk',
            partner_contribution='planned_budget.partner_contribution',
            partner_contribution_local='planned_budget.partner_contribution_local',
            partner_focal_points='-',
            partner_focal_points_data='i',
            partner_id=None,
            partner_name='agreement.partner.name',
            partner_signatory_email='partner_authorized_officer_signatory.email',
            partner_signatory_first_name='partner_authorized_officer_signatory.first_name',
            partner_signatory_last_name='partner_authorized_officer_signatory.last_name',
            partner_signatory_phone='partner_authorized_officer_signatory.phone',
            partner_signatory_title='partner_authorized_officer_signatory.title',
            partner_source_id='agreement.partner.id',
            partner_type='agreement.partner.type',
            partner_vendor_number='agreement.partner.vendor_number',
            planned_programmatic_visits='-',
            prc_review_document='=',
            sections='-',
            start_date='start',
            status='=',
            total='planned_budget.total',
            total_local='planned_budget.total_local',
            unicef_cash='planned_budget.unicef_cash',
            unicef_cash_local='planned_budget.unicef_cash_local',
            unicef_focal_points='-',
            unicef_signatory_email='unicef_signatory.email',
            unicef_signatory_first_name='unicef_signatory.first_name',
            unicef_signatory_id='unicef_signatory.pk',
            unicef_signatory_last_name='unicef_signatory.last_name',
            updated='modified',
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
