import decimal

from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices


def enrich(model: models.Model, cls):
    for attr, value in cls.__dict__.items():
        if not attr.startswith('_'):
            setattr(model, attr, value)


class TravelType:
    PROGRAMME_MONITORING = 'Programmatic Visit'
    SPOT_CHECK = 'Spot Check'
    ADVOCACY = 'Advocacy'
    TECHNICAL_SUPPORT = 'Technical Support'
    MEETING = 'Meeting'
    STAFF_DEVELOPMENT = 'Staff Development'
    STAFF_ENTITLEMENT = 'Staff Entitlement'
    CHOICES = (
        (PROGRAMME_MONITORING, 'Programmatic Visit'),
        (SPOT_CHECK, 'Spot Check'),
        (ADVOCACY, 'Advocacy'),
        (TECHNICAL_SUPPORT, 'Technical Support'),
        (MEETING, 'Meeting'),
        (STAFF_DEVELOPMENT, 'Staff Development'),
        (STAFF_ENTITLEMENT, 'Staff Entitlement'),
    )


class PartnerType:
    BILATERAL_MULTILATERAL = 'Bilateral / Multilateral'
    CIVIL_SOCIETY_ORGANIZATION = 'Civil Society Organization'
    GOVERNMENT = 'Government'
    UN_AGENCY = 'UN Agency'

    CHOICES = ((BILATERAL_MULTILATERAL, BILATERAL_MULTILATERAL),
               (CIVIL_SOCIETY_ORGANIZATION, CIVIL_SOCIETY_ORGANIZATION),
               (GOVERNMENT, GOVERNMENT),
               (UN_AGENCY, UN_AGENCY))


class PartnerOrganizationConst:
    EXPIRING_ASSESSMENT_LIMIT_YEAR = 4

    CT_CP_AUDIT_TRIGGER_LEVEL = decimal.Decimal('50000.00')

    CT_MR_AUDIT_TRIGGER_LEVEL = decimal.Decimal('2500.00')
    CT_MR_AUDIT_TRIGGER_LEVEL2 = decimal.Decimal('100000.00')
    CT_MR_AUDIT_TRIGGER_LEVEL3 = decimal.Decimal('500000.00')

    RATING_HIGH = 'High'
    RATING_SIGNIFICANT = 'Significant'
    RATING_MEDIUM = 'Medium'
    RATING_LOW = 'Low'
    RATING_NOT_REQUIRED = 'Not Required'

    RISK_RATINGS = (
        (RATING_HIGH, 'High'),
        (RATING_SIGNIFICANT, 'Significant'),
        (RATING_MEDIUM, 'Medium'),
        (RATING_LOW, 'Low'),
        (RATING_NOT_REQUIRED, 'Not Required'),
    )

    MICRO_ASSESSMENT = 'MICRO ASSESSMENT'
    HIGH_RISK_ASSUMED = 'HIGH RISK ASSUMED'
    LOW_RISK_ASSUMED = 'LOW RISK ASSUMED'
    NEGATIVE_AUDIT_RESULTS = 'NEGATIVE AUDIT RESULTS'
    SIMPLIFIED_CHECKLIST = 'SIMPLIFIED CHECKLIST'
    OTHERS = 'OTHERS'

    # maybe at some point this can become a type_of_assessment can became a choice
    TYPE_OF_ASSESSMENT = ((MICRO_ASSESSMENT, 'Micro Assessment'),
                          (HIGH_RISK_ASSUMED, 'High Risk Assumed'),
                          (LOW_RISK_ASSUMED, 'Low Risk Assumed'),
                          (NEGATIVE_AUDIT_RESULTS, 'Negative Audit Results'),
                          (SIMPLIFIED_CHECKLIST, 'Simplified Checklist'),
                          (OTHERS, 'Others'),
                          )

    AGENCY_CHOICES = (('DPKO', 'DPKO'),
                      ('ECA', 'ECA'),
                      ('ECLAC', 'ECLAC'),
                      ('ESCWA', 'ESCWA'),
                      ('FAO', 'FAO'),
                      ('ILO', 'ILO'),
                      ('IOM', 'IOM'),
                      ('OHCHR', 'OHCHR'),
                      ('UN', 'UN'),
                      ('UN Women', 'UN Women'),
                      ('UNAIDS', 'UNAIDS'),
                      ('UNDP', 'UNDP'),
                      ('UNESCO', 'UNESCO'),
                      ('UNFPA', 'UNFPA'),
                      ('UN - Habitat', 'UN - Habitat'),
                      ('UNHCR', 'UNHCR'),
                      ('UNODC', 'UNODC'),
                      ('UNOPS', 'UNOPS'),
                      ('UNRWA', 'UNRWA'),
                      ('UNSC', 'UNSC'),
                      ('UNU', 'UNU'),
                      ('WB', 'WB'),
                      ('WFP', 'WFP'),
                      ('WHO', 'WHO')
                      )

    CSO_TYPES = (('International', 'International'),
                 ('National', 'National'),
                 ('Community Based Organization', 'Community Based Organization'),
                 ('Academic Institution', 'Academic Institution'),
                 )

    ASSURANCE_VOID = 'void'
    ASSURANCE_PARTIAL = 'partial'
    ASSURANCE_COMPLETE = 'complete'


class T2FTravelConsts:
    PLANNED = 'planned'
    SUBMITTED = 'submitted'
    REJECTED = 'rejected'
    APPROVED = 'approved'
    CANCELLED = 'cancelled'
    SENT_FOR_PAYMENT = 'sent_for_payment'
    CERTIFICATION_SUBMITTED = 'certification_submitted'
    CERTIFICATION_APPROVED = 'certification_approved'
    CERTIFICATION_REJECTED = 'certification_rejected'
    CERTIFIED = 'certified'
    COMPLETED = 'completed'

    CHOICES = (
        (PLANNED, _('Planned')),
        (SUBMITTED, _('Submitted')),
        (REJECTED, _('Rejected')),
        (APPROVED, _('Approved')),
        (COMPLETED, _('Completed')),
        (CANCELLED, _('Cancelled')),
        (SENT_FOR_PAYMENT, _('Sent for payment')),
        (CERTIFICATION_SUBMITTED, _('Certification submitted')),
        (CERTIFICATION_APPROVED, _('Certification approved')),
        (CERTIFICATION_REJECTED, _('Certification rejected')),
        (CERTIFIED, _('Certified')),
        (COMPLETED, _('Completed')),
    )


class CategoryConsts:
    MODULE_CHOICES = Choices(
        ('apd', _('Action Points')),
        ('t2f', _('Trip Management')),
        ('tpm', _('Third Party Monitoring')),
        ('audit', _('Financial Assurance')),
    )


class AuditEngagementConsts:
    TYPE_AUDIT = 'audit'
    TYPE_MICRO_ASSESSMENT = 'ma'
    TYPE_SPOT_CHECK = 'sc'
    TYPE_SPECIAL_AUDIT = 'sa'

    TYPES = ((TYPE_AUDIT, _('Audit')),
             (TYPE_MICRO_ASSESSMENT, _('Micro Assessment')),
             (TYPE_SPOT_CHECK, _('Spot Check')),
             (TYPE_SPECIAL_AUDIT, _('Special Audit')),
             )

    DISPLAY_STATUSES = Choices(
        ('partner_contacted', _('IP Contacted')),
        ('field_visit', _('Field Visit')),
        ('draft_issued_to_partner', _('Draft Report Issued to IP')),
        ('comments_received_by_partner', _('Comments Received from IP')),
        ('draft_issued_to_unicef', _('Draft Report Issued to UNICEF')),
        ('comments_received_by_unicef', _('Comments Received from UNICEF')),
        ('report_submitted', _('Report Submitted')),
        ('final', _('Final Report')),
        ('cancelled', _('Cancelled')),
    )


class ActionPointConsts:
    MODULE_CHOICES = CategoryConsts.MODULE_CHOICES

    STATUS_OPEN = 'open'
    STATUS_COMPLETED = 'completed'

    STATUSES = (
        (STATUS_OPEN, _('Open')),
        (STATUS_COMPLETED, _('Completed')),
    )

    STATUSES_DATES = {
        STATUS_OPEN: 'created',
        STATUS_COMPLETED: 'date_of_completion'
    }

    KEY_EVENTS = (
        ('status_update', _('Status Update')),
        ('reassign', _('Reassign')),
    )

    MAPS = {AuditEngagementConsts.TYPE_SPOT_CHECK: 'AuditSpotcheck',
            AuditEngagementConsts.TYPE_AUDIT: 'AuditMicroassessment',
            AuditEngagementConsts.TYPE_MICRO_ASSESSMENT: 'AuditAudit',
            AuditEngagementConsts.TYPE_SPECIAL_AUDIT: 'AuditSpecialaudit',
            }


class TpmTpmvisitConst:
    DRAFT = 'draft'
    ASSIGNED = 'assigned'
    CANCELLED = 'cancelled'
    ACCEPTED = 'tpm_accepted'
    REJECTED = 'tpm_rejected'
    REPORTED = 'tpm_reported'
    REPORT_REJECTED = 'tpm_report_rejected'
    UNICEF_APPROVED = 'unicef_approved'

    STATUSES = Choices(
        (DRAFT, _('Draft')),
        (ASSIGNED, _('Assigned')),
        (CANCELLED, _('Cancelled')),
        (ACCEPTED, _('TPM Accepted')),
        (REJECTED, _('TPM Rejected')),
        (REPORTED, _('TPM Reported')),
        (REPORT_REJECTED, _('Sent Back to TPM')),
        (UNICEF_APPROVED, _('UNICEF Approved')),
    )


class PartnersAgreementConst:
    PCA = 'PCA'
    MOU = 'MOU'
    SSFA = 'SSFA'
    AGREEMENT_TYPES = (
        (PCA, "Programme Cooperation Agreement"),
        (SSFA, 'Small Scale Funding Agreement'),
        (MOU, 'Memorandum of Understanding'),
    )

    DRAFT = "draft"
    SIGNED = "signed"
    ENDED = "ended"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    STATUS_CHOICES = (
        (DRAFT, "Draft"),
        (SIGNED, "Signed"),
        (ENDED, "Ended"),
        (SUSPENDED, "Suspended"),
        (TERMINATED, "Terminated"),
    )
    AUTO_TRANSITIONS = {
        DRAFT: [SIGNED],
        SIGNED: [ENDED],
    }


class PartnersInterventionConst:
    DRAFT = 'draft'
    SIGNED = 'signed'
    ACTIVE = 'active'
    ENDED = 'ended'
    IMPLEMENTED = 'implemented'
    CLOSED = 'closed'
    SUSPENDED = 'suspended'
    TERMINATED = 'terminated'
    CANCELLED = 'cancelled'

    PD = 'PD'
    SHPD = 'SHPD'
    SSFA = 'SSFA'

    INTERVENTION_TYPES = (
        (PD, 'Programme Document'),
        (SHPD, 'Simplified Humanitarian Programme Document'),
        (SSFA, 'SSFA'),
    )
    STATUSES = (
        (DRAFT, "Draft"),
        (SIGNED, 'Signed'),
        (ACTIVE, "Active"),
        (ENDED, "Ended"),
        (CLOSED, "Closed"),
        (SUSPENDED, "Suspended"),
        (TERMINATED, "Terminated"),
        (CANCELLED, "Cancelled"),
    )