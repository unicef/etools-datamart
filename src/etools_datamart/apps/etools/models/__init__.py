# -*- coding: utf-8 -*-
from django.utils.functional import cached_property

from .public import *  # noqa
from .tenant import *  # noqa

from django.utils.translation import ugettext as _

AuditEngagement.PARTNER_CONTACTED = 'partner_contacted'
AuditEngagement.REPORT_SUBMITTED = 'report_submitted'
AuditEngagement.FINAL = 'final'
AuditEngagement.CANCELLED = 'cancelled'
AuditEngagement.STATUSES = (
    (AuditEngagement.PARTNER_CONTACTED, _('IP Contacted')),
    (AuditEngagement.REPORT_SUBMITTED, _('Report Submitted')),
    (AuditEngagement.FINAL, _('Final Report')),
    (AuditEngagement.CANCELLED, _('Cancelled')),
)

PartnersPartnerorganization.current_core_value_assessment = cached_property(
    lambda self:
    self.core_values_assessments.filter(archived=False).first())

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
