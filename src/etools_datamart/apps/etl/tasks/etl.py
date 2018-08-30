# -*- coding: utf-8 -*-
import logging

from django.db import connections
from django.db.models import Sum
from django.db.models.functions import Coalesce
from strategy_field.utils import get_attr

from etools_datamart.apps.data.models import Intervention, PMPIndicators
from etools_datamart.apps.etools.models import PartnersIntervention, PartnersPartnerorganization
from etools_datamart.apps.multitenant.postgresql.utils import clear_schemas
from etools_datamart.celery import app

logger = logging.getLogger(__name__)


@app.etl(PMPIndicators)
def load_pmp_indicator():
    connection = connections['etools']
    with clear_schemas():
        schemas = connection.get_tenants()
    PMPIndicators.objects.truncate()
    base_url = 'https://etools.unicef.org'
    created = {}

    for country in schemas:
        created[country.name] = 0
        connection.set_tenant(country)
        logger.info(u'Running on %s' % country.name)
        for partner in PartnersPartnerorganization.objects.prefetch_related(
                'partnerspartnerorganization_partners_corevaluesassessment_partner_id'):
            for intervention in PartnersIntervention.objects.filter(
                    agreement__partner=partner).select_related('partnersintervention_partners_interventionbudget_intervention_id'):
                planned_budget = getattr(intervention,
                                         'partnersintervention_partners_interventionbudget_intervention_id', None)
                fr_currencies = intervention.frs.all().values_list('currency', flat=True).distinct()
                has_assessment = bool(getattr(partner.current_core_value_assessment, 'assessment', False))
                PMPIndicators.objects.create(
                    country_id=country.pk,
                    partner_id=partner.pk,
                    intervention_id=intervention.pk,
                    **{
                        'country_name': country.name,
                        'business_area_code': country.business_area_code,
                        'partner_name': partner.name,
                        'partner_type': partner.cso_type,
                        'vendor_number': partner.vendor_number,

                        'pd_ssfa_ref': intervention.number.replace(',', '-'),
                        'pd_ssfa_status': intervention.status.title(),
                        'pd_ssfa_start_date': intervention.start,
                        'pd_ssfa_creation_date': intervention.created,
                        'pd_ssfa_end_date': intervention.end,

                        'cash_contribution': intervention.total_unicef_cash or 0,
                        'supply_contribution': intervention.total_in_kind_amount or 0,
                        'total_budget': intervention.total_budget or 0,
                        'unicef_budget': intervention.total_unicef_budget or 0,

                        'currency': intervention.planned_budget.currency if planned_budget else '-',
                        'partner_contribution': intervention.planned_budget.partner_contribution if planned_budget else '-',
                        'unicef_cash': intervention.planned_budget.unicef_cash if planned_budget else '-',
                        'in_kind_amount': intervention.planned_budget.in_kind_amount if planned_budget else '-',
                        'total': intervention.planned_budget.total if planned_budget else '-',
                        'fr_numbers_against_pd_ssfa': ' - '.join([fh.fr_number for fh in intervention.frs.all()]),
                        'fr_currencies': ', '.join(fr for fr in fr_currencies),
                        'sum_of_all_fr_planned_amount': intervention.frs.aggregate(
                            total=Coalesce(Sum('intervention_amt'), 0))['total'] if fr_currencies.count() <= 1 else '-',
                        'core_value_attached': has_assessment,
                        'partner_link': '{}/pmp/partners/{}/details'.format(base_url, partner.pk),
                        'intervention_link': '{}/pmp/interventions/{}/details'.format(base_url, intervention.pk),
                    })
                created[country.name] += 1
    return created


@app.etl(Intervention)
def load_intervention():
    connection = connections['etools']
    schemas = connection.get_tenants()
    Intervention.objects.truncate()
    created = {}
    for schema in schemas:
        connection.set_tenant(schema)
        qs = PartnersIntervention.objects.all().select_related('agreement',
                                                               'partner_authorized_officer_signatory',
                                                               'unicef_signatory',
                                                               'country_programme',
                                                               )
        for num, record in enumerate(qs, 1):
            Intervention.objects.create(country_name=schema.name,
                                        number=record.number,
                                        title=record.title,
                                        status=record.status,
                                        start_date=record.start,
                                        end_date=record.end,
                                        review_date_prc=record.review_date_prc,
                                        prc_review_document=record.prc_review_document,

                                        agreement_id=record.agreement.pk,
                                        partner_authorized_officer_signatory_id=get_attr(record,
                                                                                         'partner_authorized_officer_signatory.pk'),
                                        country_programme_id=get_attr(record, 'country_programme.pk'),
                                        intervention_id=record.pk,
                                        unicef_signatory_id=get_attr(record, 'unicef_signatory.pk'),

                                        signed_by_unicef_date=record.signed_by_unicef_date,
                                        signed_by_partner_date=record.signed_by_partner_date,
                                        population_focus=record.population_focus,
                                        signed_pd_document=record.signed_pd_document,

                                        submission_date=record.submission_date,
                                        submission_date_prc=record.submission_date_prc,

                                        unicef_signatory_first_name=get_attr(record,
                                                                             'unicef_signatory.first_name'),
                                        unicef_signatory_last_name=get_attr(record,
                                                                            'unicef_signatory.last_name'),
                                        unicef_signatory_email=get_attr(record, 'unicef_signatory.email'),

                                        partner_signatory_title=get_attr(record,
                                                                         'partner_authorized_officer_signatory.title'),
                                        partner_signatory_first_name=get_attr(record,
                                                                              'partner_authorized_officer_signatory.first_name'),
                                        partner_signatory_last_name=get_attr(record,
                                                                             'partner_authorized_officer_signatory.last_name'),
                                        partner_signatory_email=get_attr(record,
                                                                         'partner_authorized_officer_signatory.email'),
                                        partner_signatory_phone=get_attr(record,
                                                                         'partner_authorized_officer_signatory.phone'),

                                        partner_focal_point_title=get_attr(record,
                                                                           'partner_focal_point.title'),
                                        partner_focal_point_first_name=get_attr(record,
                                                                                'partner_focal_point.first_name'),
                                        partner_focal_point_last_name=get_attr(record,
                                                                               'partner_focal_point.last_name'),
                                        partner_focal_point_email=get_attr(record,
                                                                           'partner_focal_point.email'),
                                        partner_focal_point_phone=get_attr(record,
                                                                           'partner_focal_point.phone'),

                                        metadata=record.metadata,
                                        document_type=record.document_type,
                                        updated=record.modified,
                                        created=record.created,

                                        )
        created[schema.name] = num

    return created
