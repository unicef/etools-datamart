from django.db import models

from etools_datamart.apps.sources.etools.models import (
    AuditAudit,
    AuditEngagement,
    AuditEngagementActivePd,
    AuditEngagementAuthorizedOfficers,
    AuditEngagementStaffMembers,
    AuditMicroassessment,
    AuditSpecialaudit,
    AuditSpotcheck,
    AuthUser,
    PartnersIntervention,
)

from .utils import set_primary_key

# AuditEngagement.TYPE_AUDIT = 'audit'
# AuditEngagement.TYPE_MICRO_ASSESSMENT = 'ma'
# AuditEngagement.TYPE_SPOT_CHECK = 'sc'
# AuditEngagement.TYPE_SPECIAL_AUDIT = 'sa'
#
# AuditEngagement.TYPES = (
#     (AuditEngagement.TYPE_AUDIT, _('Audit')),
#     (AuditEngagement.TYPE_MICRO_ASSESSMENT, _('Micro Assessment')),
#     (AuditEngagement.TYPE_SPOT_CHECK, _('Spot Check')),
#     (AuditEngagement.TYPE_SPECIAL_AUDIT, _('Special Audit')),
# )

# AuditEngagement.PARTNER_CONTACTED = 'partner_contacted'
# AuditEngagement.REPORT_SUBMITTED = 'report_submitted'
# AuditEngagement.FINAL = 'final'
# AuditEngagement.CANCELLED = 'cancelled'
#
# AuditEngagement.STATUSES = (
#     (AuditEngagement.PARTNER_CONTACTED, _('IP Contacted')),
#     (AuditEngagement.REPORT_SUBMITTED, _('Report Submitted')),
#     (AuditEngagement.FINAL, _('Final Report')),
#     (AuditEngagement.CANCELLED, _('Cancelled')),
# )


# AuditEngagement._meta.fields['engagement_type'].choices = AuditEngagement.TYPES


# models.OneToOneField(AuditEngagement,
#                      related_name='+',
#                      on_delete=models.PROTECT).contribute_to_class(AuditSpotcheck, 'engagement')

set_primary_key(AuditSpotcheck, "engagement_ptr")
set_primary_key(AuditMicroassessment, "engagement_ptr")
set_primary_key(AuditAudit, "engagement_ptr")
set_primary_key(AuditSpecialaudit, "engagement_ptr")

models.ManyToManyField(
    AuthUser,
    related_name="engagements",
    through=AuditEngagementAuthorizedOfficers,
).contribute_to_class(AuditEngagement, "authorized_officers")

models.ManyToManyField(
    AuthUser,
    through=AuditEngagementStaffMembers,
).contribute_to_class(AuditEngagement, "staff_members")

models.ManyToManyField(
    PartnersIntervention,
    through=AuditEngagementActivePd,
).contribute_to_class(AuditEngagement, "active_pd")
