from django.db import models
from django.utils.functional import cached_property

from etools_datamart.apps.etools.enrichment.utils import create_alias
from etools_datamart.apps.etools.models import PartnersIntervention, LocationsLocation, \
    PartnersInterventionFlatLocations

PartnersIntervention.total_unicef_cash = cached_property(
    lambda self: self.planned_budget.unicef_cash_local if hasattr(self, 'planned_budget') else 0)

PartnersIntervention.total_in_kind_amount = cached_property(
    lambda self: self.planned_budget.in_kind_amount_local if hasattr(self, 'planned_budget') else 0)

PartnersIntervention.total_budget = cached_property(
    lambda self: self.total_unicef_cash + self.total_partner_contribution + self.total_in_kind_amount)

PartnersIntervention.total_partner_contribution = cached_property(
    lambda self: self.planned_budget.partner_contribution_local if hasattr(self, 'planned_budget') else 0)

PartnersIntervention.total_unicef_budget = cached_property(
    lambda self: self.total_unicef_cash + self.total_in_kind_amount)

PartnersIntervention.DRAFT = 'draft'
PartnersIntervention.SIGNED = 'signed'
PartnersIntervention.ACTIVE = 'active'
PartnersIntervention.ENDED = 'ended'
PartnersIntervention.IMPLEMENTED = 'implemented'
PartnersIntervention.CLOSED = 'closed'
PartnersIntervention.SUSPENDED = 'suspended'
PartnersIntervention.TERMINATED = 'terminated'
PartnersIntervention.CANCELLED = 'cancelled'

PartnersIntervention.STATUSES = (
    (PartnersIntervention.DRAFT, "Draft"),
    (PartnersIntervention.SIGNED, 'Signed'),
    (PartnersIntervention.ACTIVE, "Active"),
    (PartnersIntervention.ENDED, "Ended"),
    (PartnersIntervention.CLOSED, "Closed"),
    (PartnersIntervention.SUSPENDED, "Suspended"),
    (PartnersIntervention.TERMINATED, "Terminated"),
    (PartnersIntervention.CANCELLED, "Cancelled"),
)
PartnersIntervention.PD = 'PD'
PartnersIntervention.SHPD = 'SHPD'
PartnersIntervention.SSFA = 'SSFA'

PartnersIntervention.INTERVENTION_TYPES = (
    (PartnersIntervention.PD, 'Programme Document'),
    (PartnersIntervention.SHPD, 'Simplified Humanitarian Programme Document'),
    (PartnersIntervention.SSFA, 'SSFA'),
)
models.ManyToManyField(LocationsLocation,
                       through=PartnersInterventionFlatLocations,
                       ).contribute_to_class(PartnersIntervention, 'flat_locations')

aliases = (['partnersintervention_partners_interventionbudget_intervention_id',
            'planned_budget'], ['partnersintervention_funds_fundsreservationheader_intervention_id',
                                'frs'])
create_alias(PartnersIntervention, aliases)
