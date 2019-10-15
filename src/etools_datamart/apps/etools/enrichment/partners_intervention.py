from django.db import models

from etools_datamart.apps.etools.enrichment.utils import create_alias
from etools_datamart.apps.etools.models import (AuthUser, LocationsLocation, PartnersIntervention,
                                                PartnersInterventionFlatLocations, PartnersInterventionOffices,
                                                PartnersInterventionPartnerFocalPoints, PartnersInterventionresultlink,
                                                PartnersInterventionSections, PartnersInterventionUnicefFocalPoints,
                                                PartnersPartnerstaffmember, ReportsResult, ReportsSector, UsersOffice,)

PartnersIntervention.total_unicef_cash = property(
    lambda self: self.planned_budget.unicef_cash_local if hasattr(self, 'planned_budget') else 0)

PartnersIntervention.total_in_kind_amount = property(
    lambda self: self.planned_budget.in_kind_amount_local if hasattr(self, 'planned_budget') else 0)

PartnersIntervention.total_budget = property(
    lambda self: self.total_unicef_cash + self.total_partner_contribution + self.total_in_kind_amount)

PartnersIntervention.total_partner_contribution = property(
    lambda self: self.planned_budget.partner_contribution_local if hasattr(self, 'planned_budget') else 0)

PartnersIntervention.total_unicef_budget = property(
    lambda self: self.total_unicef_cash + self.total_in_kind_amount)


models.ManyToManyField(LocationsLocation,
                       through=PartnersInterventionFlatLocations,
                       ).contribute_to_class(PartnersIntervention, 'flat_locations')

models.ManyToManyField(AuthUser,
                       through=PartnersInterventionUnicefFocalPoints,
                       ).contribute_to_class(PartnersIntervention, 'unicef_focal_points')

models.ManyToManyField(PartnersPartnerstaffmember,
                       through=PartnersInterventionPartnerFocalPoints,
                       ).contribute_to_class(PartnersIntervention, 'partner_focal_points')

models.ManyToManyField(UsersOffice,
                       through=PartnersInterventionOffices,
                       ).contribute_to_class(PartnersIntervention, 'offices')

models.ManyToManyField(ReportsSector,
                       through=PartnersInterventionSections,
                       ).contribute_to_class(PartnersIntervention, 'sections')

models.ManyToManyField(ReportsResult,
                       through=PartnersInterventionresultlink,
                       ).contribute_to_class(PartnersIntervention, 'result_links')

# models.ManyToManyField(PartnersInterventionattachment,
#                        through=PartnersInterventionAttachment,
#                        ).contribute_to_class(PartnersIntervention, 'attachments')

aliases = (['partnersintervention_partners_interventionbudget_intervention_id',
            'planned_budget'],
           ['partnersintervention_funds_fundsreservationheader_intervention_id',
            'frs'],
           ['partnersintervention_partners_interventionattachment_intervention_id',
            'attachments'],

           # ['partnersintervention_partners_interventionplannedvisits_intervention_id',
           #  'planned_visits'],

           )
create_alias(PartnersIntervention, aliases)


def reference_number(self):
    return self.number
    # if self.document_type != PartnersIntervention.SSFA:
    #     number = '{agreement}/{type}{year}{id}'.format(
    #         agreement=self.agreement.base_number,
    #         type=self.document_type,
    #         year=self.reference_number_year,
    #         id=self.id
    #     )
    #     return number
    # return self.agreement.base_number


PartnersIntervention.reference_number = property(reference_number)
