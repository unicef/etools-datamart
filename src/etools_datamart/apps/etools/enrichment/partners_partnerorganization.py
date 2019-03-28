from django.utils.functional import cached_property

from etools_datamart.apps.etools.models import PartnersPartnerorganization

from .utils import create_alias

PartnersPartnerorganization.CSO_TYPES = (
    ('International', 'International'),
    ('National', 'National'),
    ('Community Based Organization', 'Community Based Organization'),
    ('Academic Institution', 'Academic Institution'),
)

PartnersPartnerorganization.current_core_value_assessment = cached_property(
    lambda self:
    self.core_values_assessments.filter(archived=False).first())

aliases = (
    # CoreValuesAssessment.partner
    ['partnerspartnerorganization_partners_corevaluesassessment_partner_id',
     'core_values_assessments'],
    # PlannedEngagement
    # ['partnerspartnerorganization_partners_plannedengagement_partner_id',
    #  'planned_engagement'],
)
create_alias(PartnersPartnerorganization, aliases)
