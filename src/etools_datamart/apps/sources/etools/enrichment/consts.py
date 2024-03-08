import decimal

from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices


def enrich(model: models.Model, cls):
    for attr, value in cls.__dict__.items():
        if not attr.startswith("_"):
            setattr(model, attr, value)


class TravelType:
    PROGRAMME_MONITORING = "Programmatic Visit"
    SPOT_CHECK = "Spot Check"
    ADVOCACY = "Advocacy"
    TECHNICAL_SUPPORT = "Technical Support"
    MEETING = "Meeting"
    STAFF_DEVELOPMENT = "Staff Development"
    STAFF_ENTITLEMENT = "Staff Entitlement"
    CHOICES = (
        (PROGRAMME_MONITORING, "Programmatic Visit"),
        (SPOT_CHECK, "Spot Check"),
        (ADVOCACY, "Advocacy"),
        (TECHNICAL_SUPPORT, "Technical Support"),
        (MEETING, "Meeting"),
        (STAFF_DEVELOPMENT, "Staff Development"),
        (STAFF_ENTITLEMENT, "Staff Entitlement"),
    )


class PartnerType:
    BILATERAL_MULTILATERAL = "Bilateral / Multilateral"
    CIVIL_SOCIETY_ORGANIZATION = "Civil Society Organization"
    GOVERNMENT = "Government"
    UN_AGENCY = "UN Agency"

    CHOICES = (
        (BILATERAL_MULTILATERAL, BILATERAL_MULTILATERAL),
        (CIVIL_SOCIETY_ORGANIZATION, CIVIL_SOCIETY_ORGANIZATION),
        (GOVERNMENT, GOVERNMENT),
        (UN_AGENCY, UN_AGENCY),
    )


class PartnerOrganizationConst:
    EXPIRING_ASSESSMENT_LIMIT_YEAR = 4

    CT_CP_AUDIT_TRIGGER_LEVEL = decimal.Decimal("50000.00")

    CT_MR_AUDIT_TRIGGER_LEVEL = decimal.Decimal("2500.00")
    CT_MR_AUDIT_TRIGGER_LEVEL2 = decimal.Decimal("100000.00")
    CT_MR_AUDIT_TRIGGER_LEVEL3 = decimal.Decimal("500000.00")

    RATING_HIGH = "High"
    RATING_SIGNIFICANT = "Significant"
    RATING_MEDIUM = "Medium"
    RATING_LOW = "Low"
    RATING_NOT_REQUIRED = "Not Required"

    PSEA_RATING_HIGH = "Low Capacity (High Risk)"
    PSEA_RATING_MEDIUM = "Medium Capacity (Moderate Risk)"
    PSEA_RATING_LOW = "Full Capacity (Low Risk)"
    RATING_HIGH_RISK_ASSUMED = "Low Capacity Assumed - Emergency"
    RATING_LOW_RISK_ASSUMED = "No Contact with Beneficiaries"
    RATING_NOT_ASSESSED = "Not Assessed"

    RISK_RATINGS = (
        (RATING_HIGH, "High"),
        (RATING_SIGNIFICANT, "Significant"),
        (RATING_MEDIUM, "Medium"),
        (RATING_LOW, "Low"),
        (RATING_NOT_REQUIRED, "Not Required"),
    )

    MICRO_ASSESSMENT = "MICRO ASSESSMENT"
    HIGH_RISK_ASSUMED = "HIGH RISK ASSUMED"
    LOW_RISK_ASSUMED = "LOW RISK ASSUMED"
    NEGATIVE_AUDIT_RESULTS = "NEGATIVE AUDIT RESULTS"
    SIMPLIFIED_CHECKLIST = "SIMPLIFIED CHECKLIST"
    OTHERS = "OTHERS"

    # maybe at some point this can become a type_of_assessment can became a choice
    TYPE_OF_ASSESSMENT = (
        (MICRO_ASSESSMENT, "Micro Assessment"),
        (HIGH_RISK_ASSUMED, "High Risk Assumed"),
        (LOW_RISK_ASSUMED, "Low Risk Assumed"),
        (NEGATIVE_AUDIT_RESULTS, "Negative Audit Results"),
        (SIMPLIFIED_CHECKLIST, "Simplified Checklist"),
        (OTHERS, "Others"),
    )

    AGENCY_CHOICES = (
        ("DPKO", "DPKO"),
        ("ECA", "ECA"),
        ("ECLAC", "ECLAC"),
        ("ESCWA", "ESCWA"),
        ("FAO", "FAO"),
        ("ILO", "ILO"),
        ("IOM", "IOM"),
        ("OHCHR", "OHCHR"),
        ("UN", "UN"),
        ("UN Women", "UN Women"),
        ("UNAIDS", "UNAIDS"),
        ("UNDP", "UNDP"),
        ("UNESCO", "UNESCO"),
        ("UNFPA", "UNFPA"),
        ("UN - Habitat", "UN - Habitat"),
        ("UNHCR", "UNHCR"),
        ("UNODC", "UNODC"),
        ("UNOPS", "UNOPS"),
        ("UNRWA", "UNRWA"),
        ("UNSC", "UNSC"),
        ("UNU", "UNU"),
        ("WB", "WB"),
        ("WFP", "WFP"),
        ("WHO", "WHO"),
    )

    CSO_TYPES = (
        ("International", "International"),
        ("National", "National"),
        ("Community Based Organization", "Community Based Organization"),
        ("Academic Institution", "Academic Institution"),
    )

    ASSURANCE_VOID = "void"
    ASSURANCE_PARTIAL = "partial"
    ASSURANCE_COMPLETE = "complete"


class T2FTravelConsts:
    PLANNED = "planned"
    SUBMITTED = "submitted"
    REJECTED = "rejected"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    SENT_FOR_PAYMENT = "sent_for_payment"
    CERTIFICATION_SUBMITTED = "certification_submitted"
    CERTIFICATION_APPROVED = "certification_approved"
    CERTIFICATION_REJECTED = "certification_rejected"
    CERTIFIED = "certified"
    COMPLETED = "completed"

    CHOICES = (
        (PLANNED, _("Planned")),
        (SUBMITTED, _("Submitted")),
        (REJECTED, _("Rejected")),
        (APPROVED, _("Approved")),
        (COMPLETED, _("Completed")),
        (CANCELLED, _("Cancelled")),
        (SENT_FOR_PAYMENT, _("Sent for payment")),
        (CERTIFICATION_SUBMITTED, _("Certification submitted")),
        (CERTIFICATION_APPROVED, _("Certification approved")),
        (CERTIFICATION_REJECTED, _("Certification rejected")),
        (CERTIFIED, _("Certified")),
        (COMPLETED, _("Completed")),
    )


class TravelTripConsts:
    STATUS_DRAFT = "draft"
    STATUS_SUBMISSION_REVIEW = "submission"
    STATUS_SUBMITTED = "submitted"
    STATUS_REJECTED = "rejected"
    STATUS_APPROVED = "approved"
    STATUS_REVIEW = "review"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    CHOICES = (
        (STATUS_DRAFT, _("Draft")),
        (STATUS_SUBMISSION_REVIEW, _("Submission Review")),
        (STATUS_SUBMITTED, _("Submitted")),
        (STATUS_REJECTED, _("Rejected")),
        (STATUS_APPROVED, _("Approved")),
        (STATUS_REVIEW, _("Review")),
        (STATUS_COMPLETED, _("Completed")),
        (STATUS_CANCELLED, _("Cancelled")),
    )


class CategoryConsts:
    MODULE_CHOICES = Choices(
        ("apd", _("Action Points")),
        ("t2f", _("Trip Management")),
        ("tpm", _("Third Party Monitoring")),
        ("audit", _("Financial Assurance")),
        ("psea", _("PSEA Assessment")),
        ("fm", _("Field Monitoring")),
    )


class AuditEngagementConsts:
    TYPE_AUDIT = "audit"
    TYPE_MICRO_ASSESSMENT = "ma"
    TYPE_SPOT_CHECK = "sc"
    TYPE_SPECIAL_AUDIT = "sa"

    TYPES = (
        (TYPE_AUDIT, _("Audit")),
        (TYPE_MICRO_ASSESSMENT, _("Micro Assessment")),
        (TYPE_SPOT_CHECK, _("Spot Check")),
        (TYPE_SPECIAL_AUDIT, _("Special Audit")),
    )

    PARTNER_CONTACTED = "partner_contacted"
    REPORT_SUBMITTED = "report_submitted"
    FINAL = "final"
    CANCELLED = "cancelled"

    STATUSES = Choices(
        (PARTNER_CONTACTED, _("IP Contacted")),
        (REPORT_SUBMITTED, _("Report Submitted")),
        (FINAL, _("Final Report")),
        (CANCELLED, _("Cancelled")),
    )

    DISPLAY_STATUSES = Choices(
        ("partner_contacted", _("IP Contacted")),
        ("field_visit", _("Field Visit")),
        ("draft_issued_to_partner", _("Draft Report Issued to IP")),
        ("comments_received_by_partner", _("Comments Received from IP")),
        ("draft_issued_to_unicef", _("Draft Report Issued to UNICEF")),
        ("comments_received_by_unicef", _("Comments Received from UNICEF")),
        ("report_submitted", _("Report Submitted")),
        ("final", _("Final Report")),
        ("cancelled", _("Cancelled")),
    )
    DISPLAY_STATUSES_DATES = {
        DISPLAY_STATUSES.partner_contacted: "partner_contacted_at",
        DISPLAY_STATUSES.field_visit: "date_of_field_visit",
        DISPLAY_STATUSES.draft_issued_to_partner: "date_of_draft_report_to_ip",
        DISPLAY_STATUSES.comments_received_by_partner: "date_of_comments_by_ip",
        DISPLAY_STATUSES.draft_issued_to_unicef: "date_of_draft_report_to_unicef",
        DISPLAY_STATUSES.comments_received_by_unicef: "date_of_comments_by_unicef",
        DISPLAY_STATUSES.report_submitted: "date_of_report_submit",
        DISPLAY_STATUSES.final: "date_of_final_report",
        DISPLAY_STATUSES.cancelled: "date_of_cancel",
    }


class AuditFinancialFindingsConsts:
    TITLE_CHOICES = Choices(
        ("no-supporting-documentation", _("No supporting documentation")),
        ("insufficient-supporting-documentation", _("Insufficient supporting documentation")),
        ("cut-off-error", _("Cut-off error")),
        ("expenditure-not-for-project-purposes", _("Expenditure not for project purposes")),
        ("no-proof-of-payment", _("No proof of payment")),
        ("no-proof-of-goods-services-received", _("No proof of goods / services received")),
        ("vat-incorrectly-claimed", _("VAT incorrectly claimed")),
        ("dsa-rates-exceeded", _("DSA rates exceeded")),
        ("unreasonable-price", _("Unreasonable price")),
        ("bank-interest-not-reported", _("Bank interest not reported")),
        ("support-costs-incorrectly-calculated", _("Support costs incorrectly calculated")),
        ("expenditure-claimed-but-activities-not-undertaken", _("Expenditure claimed but activities not undertaken")),
        ("advance-claimed-as-expenditure", _("Advance claimed as expenditure")),
        ("commitments-treated-as-expenditure", _("Commitments treated as expenditure")),
        ("ineligible-salary-costs", _("Ineligible salary costs")),
        ("ineligible-costs-other", _("Ineligible costs (other)")),
    )


class ActionPointConsts:
    MODULE_CHOICES = CategoryConsts.MODULE_CHOICES

    STATUS_OPEN = "open"
    STATUS_COMPLETED = "completed"

    STATUSES = (
        (STATUS_OPEN, _("Open")),
        (STATUS_COMPLETED, _("Completed")),
    )

    STATUSES_DATES = {STATUS_OPEN: "created", STATUS_COMPLETED: "date_of_completion"}

    KEY_EVENTS = (
        ("status_update", _("Status Update")),
        ("reassign", _("Reassign")),
    )

    MAPS = {
        AuditEngagementConsts.TYPE_SPOT_CHECK: "AuditSpotcheck",
        AuditEngagementConsts.TYPE_AUDIT: "AuditMicroassessment",
        AuditEngagementConsts.TYPE_MICRO_ASSESSMENT: "AuditAudit",
        AuditEngagementConsts.TYPE_SPECIAL_AUDIT: "AuditSpecialaudit",
    }


class TpmTpmvisitConst:
    DRAFT = "draft"
    ASSIGNED = "assigned"
    CANCELLED = "cancelled"
    ACCEPTED = "tpm_accepted"
    REJECTED = "tpm_rejected"
    REPORTED = "tpm_reported"
    REPORT_REJECTED = "tpm_report_rejected"
    UNICEF_APPROVED = "unicef_approved"

    STATUSES = Choices(
        (DRAFT, _("Draft")),
        (ASSIGNED, _("Assigned")),
        (CANCELLED, _("Cancelled")),
        (ACCEPTED, _("TPM Accepted")),
        (REJECTED, _("TPM Rejected")),
        (REPORTED, _("TPM Reported")),
        (REPORT_REJECTED, _("Sent Back to TPM")),
        (UNICEF_APPROVED, _("UNICEF Approved")),
    )


class PartnersAgreementConst:
    PCA = "PCA"
    MOU = "MOU"
    SSFA = "SSFA"
    AGREEMENT_TYPES = (
        (PCA, "Programme Cooperation Agreement"),
        (SSFA, "Small Scale Funding Agreement"),
        (MOU, "Memorandum of Understanding"),
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
    DRAFT = "draft"
    SIGNED = "signed"
    ACTIVE = "active"
    ENDED = "ended"
    IMPLEMENTED = "implemented"
    CLOSED = "closed"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    CANCELLED = "cancelled"

    PD = "PD"
    SPD = "SPD"
    SSFA = "SSFA"

    INTERVENTION_TYPES = (
        (PD, "Programme Document"),
        (SPD, "Simplified Programme Document"),
        # (SSFA, "SSFA"),
    )
    STATUSES = (
        (DRAFT, "Draft"),
        (SIGNED, "Signed"),
        (ACTIVE, "Active"),
        (ENDED, "Ended"),
        (CLOSED, "Closed"),
        (SUSPENDED, "Suspended"),
        (TERMINATED, "Terminated"),
        (CANCELLED, "Cancelled"),
    )


class RiskConst:
    VALUES = Choices(
        (0, "na", "N/A"),
        (1, "low", "Low"),
        (2, "medium", "Medium"),
        (3, "significant", "Significant"),
        (4, "high", "High"),
    )


class FieldMonitoringPlanningMonitoringactivityConst:
    STATUS_COMPLETED = "completed"
