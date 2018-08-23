# -*- coding: utf-8 -*-
from django.apps import AppConfig


def create_alias(model, aliases):
    for related, business_name in aliases:
        r = getattr(model, related)
        setattr(model, business_name, r)


class Config(AppConfig):
    name = 'etools_datamart.apps.etl'

    def ready(self):
        pass
        from etools_datamart.apps.etools.models import (PartnersPartnerorganization,
                                                        PartnersIntervention)

        aliases = (['partnerspartnerorganization_partners_corevaluesassessment_partner_id',
                    'core_values_assessments'],)
        create_alias(PartnersPartnerorganization, aliases)

        aliases = (['partnersintervention_partners_interventionbudget_intervention_id',
                    'planned_budget'], ['partnersintervention_funds_fundsreservationheader_intervention_id',
                                        'frs'])
        create_alias(PartnersIntervention, aliases)
