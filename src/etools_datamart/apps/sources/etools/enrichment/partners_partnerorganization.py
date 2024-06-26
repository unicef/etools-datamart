from etools_datamart.apps.sources.etools.models import (
    AuditSpotcheck,
    PartnersPartnerorganization,
    PartnersPlannedengagement,
)

from .consts import PartnerOrganizationConst, PartnerType
from .utils import create_alias

PartnersPartnerorganization.CSO_TYPES = (
    ("International", "International"),
    ("National", "National"),
    ("Community Based Organization", "Community Based Organization"),
    ("Academic Institution", "Academic Institution"),
)

PartnersPartnerorganization.current_core_value_assessment = property(
    lambda self: self.PartnersCorevaluesassessment_partner.filter(archived=False).first()
)

aliases = (
    # CoreValuesAssessment.partner
    ["partnerspartnerorganization_partners_corevaluesassessment_partner_id", "core_values_assessments"],
    # PlannedEngagement
    # ['partnerspartnerorganization_partners_plannedengagement_partner_id',
    #  'planned_engagement'],
)


def min_req_programme_visits(self):
    programme_visits = 0
    if self.organization.organization_type not in [PartnerType.BILATERAL_MULTILATERAL, PartnerType.UN_AGENCY]:
        ct = self.net_ct_cy or 0  # Must be integer, but net_ct_cy could be None

        if ct <= PartnerOrganizationConst.CT_MR_AUDIT_TRIGGER_LEVEL:
            programme_visits = 0
        elif (
            PartnerOrganizationConst.CT_MR_AUDIT_TRIGGER_LEVEL
            < ct
            <= PartnerOrganizationConst.CT_MR_AUDIT_TRIGGER_LEVEL2
        ):
            programme_visits = 1
        elif (
            PartnerOrganizationConst.CT_MR_AUDIT_TRIGGER_LEVEL2
            < ct
            <= PartnerOrganizationConst.CT_MR_AUDIT_TRIGGER_LEVEL3
        ):
            if self.highest_risk_rating_name in [
                PartnerOrganizationConst.RATING_HIGH,
                PartnerOrganizationConst.PSEA_RATING_HIGH,
                PartnerOrganizationConst.RATING_HIGH_RISK_ASSUMED,
                PartnerOrganizationConst.RATING_SIGNIFICANT,
            ]:
                programme_visits = 3
            elif self.highest_risk_rating_name in [
                PartnerOrganizationConst.RATING_MEDIUM,
                PartnerOrganizationConst.PSEA_RATING_MEDIUM,
            ]:
                programme_visits = 2
            elif self.highest_risk_rating_name in [
                PartnerOrganizationConst.RATING_LOW,
                PartnerOrganizationConst.RATING_LOW_RISK_ASSUMED,
                PartnerOrganizationConst.PSEA_RATING_LOW,
            ]:
                programme_visits = 1
        else:
            if self.highest_risk_rating_name in [
                PartnerOrganizationConst.RATING_HIGH,
                PartnerOrganizationConst.PSEA_RATING_HIGH,
                PartnerOrganizationConst.RATING_HIGH_RISK_ASSUMED,
                PartnerOrganizationConst.RATING_SIGNIFICANT,
            ]:
                programme_visits = 4
            elif self.highest_risk_rating_name in [
                PartnerOrganizationConst.RATING_MEDIUM,
                PartnerOrganizationConst.PSEA_RATING_MEDIUM,
            ]:
                programme_visits = 3
            elif self.highest_risk_rating_name in [
                PartnerOrganizationConst.RATING_LOW,
                PartnerOrganizationConst.RATING_LOW_RISK_ASSUMED,
                PartnerOrganizationConst.PSEA_RATING_LOW,
            ]:
                programme_visits = 2
    return programme_visits


PartnersPartnerorganization.min_req_programme_visits = property(min_req_programme_visits)


def min_req_spot_checks(self):
    # reported_cy can be None
    reported_cy = self.reported_cy or 0
    if self.partner_type in [PartnerType.BILATERAL_MULTILATERAL, PartnerType.UN_AGENCY]:
        return 0
    if (
        self.type_of_assessment == "Low Risk Assumed"
        or reported_cy <= PartnerOrganizationConst.CT_CP_AUDIT_TRIGGER_LEVEL
    ):
        return 0

    try:
        self.PartnersPlannedengagement_partner
    except PartnersPlannedengagement.DoesNotExist:
        pass
    else:
        if self.planned_engagement.scheduled_audit:
            return 0
    return 1


PartnersPartnerorganization.min_req_spot_checks = property(min_req_spot_checks)


def min_req_audits(self):
    return self.planned_engagement.required_audit if getattr(self, "planned_engagement", None) else 0


PartnersPartnerorganization.min_req_audits = property(min_req_audits)


def hact_min_requirements(self):
    return {
        "programme_visits": self.min_req_programme_visits,
        "spot_checks": self.min_req_spot_checks,
        "audits": self.min_req_audits,
    }


PartnersPartnerorganization.hact_min_requirements = property(hact_min_requirements)

create_alias(PartnersPartnerorganization, aliases)
PartnersPartnerorganization.spotchecks = property(
    lambda self: AuditSpotcheck.objects.filter(engagement_ptr__partner=self)
)
# partnerspartnerorganization_audit_engagement_partner_id

# add_m2m(PartnersPartnerorganization, 'spotchecks', AuditSpotcheck)
