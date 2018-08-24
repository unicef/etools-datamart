# -*- coding: utf-8 -*-
import logging

from django.db import connections
from django.db.models import Sum
from django.db.models.functions import Coalesce

from etools_datamart.apps.data.models import PMPIndicators
from etools_datamart.apps.etools.models import PartnersIntervention, PartnersPartnerorganization
from etools_datamart.apps.multitenant.postgresql.utils import clear_schemas
from etools_datamart.celery import app

logger = logging.getLogger(__name__)


@app.task()
def load_pmp_indicator():
    # qs = UsersCountry.objects.exclude(schema_name__in=['public', 'uat', 'frg'])
    connection = connections['etools']
    with clear_schemas():
        schemas = connection.get_tenants()
    PMPIndicators.objects.truncate()
    base_url = 'https://etools.unicef.org'
    for country in schemas:
        connection.set_tenant(country)
        logger.info(u'Running on %s' % country.name)
        for partner in PartnersPartnerorganization.objects.prefetch_related('partnerspartnerorganization_partners_corevaluesassessment_partner_id'):
            for intervention in PartnersIntervention.objects.filter(
                    agreement__partner=partner).select_related('partnersintervention_partners_interventionbudget_intervention_id'):
                planned_budget = getattr(intervention, 'partnersintervention_partners_interventionbudget_intervention_id', None)
                fr_currencies = intervention.frs.all().values_list('currency', flat=True).distinct()
                has_assessment = bool(getattr(partner.current_core_value_assessment, 'assessment', False))
                PMPIndicators.objects.update_or_create(
                    country_id=country.pk,
                    partner_id=partner.pk,
                    intervention_id=intervention.pk,
                    defaults={
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
