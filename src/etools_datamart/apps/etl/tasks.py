# -*- coding: utf-8 -*-
import logging

from django.db import connection, connections
from django.db.models import Sum
from django.db.models.functions import Coalesce

from etools_datamart.apps.data.models import PMPIndicators
from etools_datamart.apps.etools.models import (PartnersIntervention,
                                                PartnersPartnerorganization,
                                                UsersCountry)

logger = logging.getLogger(__name__)


def load_pmp_indicator():
    # FIXME: remove this line (pdb)
    import pdb; pdb.set_trace()
    qs = UsersCountry.objects.exclude(schema_name__in=['public', 'uat', 'frg'])
    base_url = 'https://etools.unicef.org'
    connection = connections['etools']
    for country in qs:
        connection.set_tenant(UsersCountry.objects.get(name=country.name))
        logger.info(u'Running on %s' % country.name)
        for partner in PartnersPartnerorganization.objects.prefetch_related('core_values_assessments'):
            for intervention in PartnersIntervention.objects.filter(
                    agreement__partner=partner).select_related('planned_budget'):
                planned_budget = getattr(intervention, 'planned_budget', None)
                fr_currencies = intervention.frs.all().values_list('currency', flat=True).distinct()
                has_assessment = bool(getattr(partner.current_core_value_assessment, 'assessment', False))
                PMPIndicators.objects.create(
                    **{'country': country,
                       'partner': partner,
                       'intervention': intervention,

                       'country_name': country,
                       'partner_name': str(partner),
                       'partner_type': partner.cso_type,
                       'pd_ssfa_ref': intervention.number.replace(',', '-'),
                       'pd_sfa_status': intervention.get_status_display(),
                       'pd_ssfa_start_date': intervention.start,
                       'pd_ssfa_creation_date': intervention.created,
                       'pd_ssfa_end date': intervention.end,
                       'cash_contribution': intervention.total_unicef_cash,
                       'supply_contribution': intervention.total_in_kind_amount,
                       'total_budget': intervention.total_budget,
                       'unicef_budget': intervention.total_unicef_budget,
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
