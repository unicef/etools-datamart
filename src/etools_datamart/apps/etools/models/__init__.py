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


# AuthUser.groups = property(lambda self: AuthGroup.objects.filter(users=self))
f = [f for f in AuthUserGroups._meta.local_fields if f.name != 'user_id']
AuthUserGroups._meta.local_fields = f
AuthUserGroups._meta.unique_together = []
models.ForeignKey(AuthUser, on_delete=models.PROTECT).contribute_to_class(AuthUserGroups, 'user')
models.ManyToManyField(AuthGroup,
                       through=AuthUserGroups,
                       ).contribute_to_class(AuthUser, 'groups')


# groups = models.ManyToManyField(
#     Group,
#     verbose_name=_('groups'),
#     blank=True,
#     help_text=_(
#         'The groups this user belongs to. A user will get all permissions '
#         'granted to each of their groups.'
#     ),
#     related_name="user_set",
#     related_query_name="user",
# )
# user_permissions = models.ManyToManyField(
#     Permission,
#     verbose_name=_('user permissions'),
#     blank=True,
#     help_text=_('Specific permissions for this user.'),
#     related_name="user_set",
#     related_query_name="user",
# )
