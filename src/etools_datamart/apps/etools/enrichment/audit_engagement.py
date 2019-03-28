from django.utils.translation import gettext as _

from etools_datamart.apps.etools.models import AuditEngagement

AuditEngagement.TYPE_AUDIT = 'audit'
AuditEngagement.TYPE_MICRO_ASSESSMENT = 'ma'
AuditEngagement.TYPE_SPOT_CHECK = 'sc'
AuditEngagement.TYPE_SPECIAL_AUDIT = 'sa'

AuditEngagement.TYPES = (
    (AuditEngagement.TYPE_AUDIT, _('Audit')),
    (AuditEngagement.TYPE_MICRO_ASSESSMENT, _('Micro Assessment')),
    (AuditEngagement.TYPE_SPOT_CHECK, _('Spot Check')),
    (AuditEngagement.TYPE_SPECIAL_AUDIT, _('Special Audit')),
)

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
# AuditEngagement._meta.fields['engagement_type'].choices = AuditEngagement.TYPES
