# -*- coding: utf-8 -*-
# flake8: noqa F405
import decimal
from functools import partial, partialmethod

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

from unicef_security.models import User

from etools_datamart.apps.etools.models import (LocationsLocation, PartnersPlannedengagement,
                                                ReportsAppliedindicator, ReportsAppliedindicatorDisaggregation,
                                                ReportsAppliedindicatorLocations, ReportsDisaggregation, T2FTravel,)


def label(attr, self):
    return getattr(self, attr)


def create_alias(model, aliases):
    for related, business_name in aliases:
        r = getattr(model, related)
        setattr(model, business_name, r)

    # for related, business_name in aliases:
    #     opts = model._meta
    #     fld = opts.get_field(related)
    #     fld.related_name = business_name
    #     setattr(model, business_name, fld)


T2FTravel_PLANNED = 'planned'
T2FTravel_SUBMITTED = 'submitted'
T2FTravel_REJECTED = 'rejected'
T2FTravel_APPROVED = 'approved'
T2FTravel_CANCELLED = 'cancelled'
T2FTravel_SENT_FOR_PAYMENT = 'sent_for_payment'
T2FTravel_CERTIFICATION_SUBMITTED = 'certification_submitted'
T2FTravel_CERTIFICATION_APPROVED = 'certification_approved'
T2FTravel_CERTIFICATION_REJECTED = 'certification_rejected'
T2FTravel_CERTIFIED = 'certified'
T2FTravel_COMPLETED = 'completed'

T2FTravel_CHOICES = (
    (T2FTravel_PLANNED, _('Planned')),
    (T2FTravel_SUBMITTED, _('Submitted')),
    (T2FTravel_REJECTED, _('Rejected')),
    (T2FTravel_APPROVED, _('Approved')),
    (T2FTravel_COMPLETED, _('Completed')),
    (T2FTravel_CANCELLED, _('Cancelled')),
    (T2FTravel_SENT_FOR_PAYMENT, _('Sent for payment')),
    (T2FTravel_CERTIFICATION_SUBMITTED, _('Certification submitted')),
    (T2FTravel_CERTIFICATION_APPROVED, _('Certification approved')),
    (T2FTravel_CERTIFICATION_REJECTED, _('Certification rejected')),
    (T2FTravel_CERTIFIED, _('Certified')),
    (T2FTravel_COMPLETED, _('Completed')),
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


class PartnerOrganization:
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


def patch():
    from django.apps import apps
    from .models import (AuditEngagement, AuthGroup, AuthUser, AuthUserGroups, PartnersIntervention,
                         PartnersPartnerorganization, UsersCountry, UsersUserprofile,
                         UsersUserprofileCountriesAvailable, )

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
    PartnersPartnerorganization.CSO_TYPES = (
        ('International', 'International'),
        ('National', 'National'),
        ('Community Based Organization', 'Community Based Organization'),
        ('Academic Institution', 'Academic Institution'),
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
    # Fix User OneToOneField
    # for model in [AuthUserGroups, UsersUserprofile]:

    f = [f for f in AuthUserGroups._meta.local_fields if f.name != 'user_id']
    AuthUserGroups._meta.local_fields = f
    AuthUserGroups._meta.unique_together = []
    models.OneToOneField(AuthUser,
                         on_delete=models.PROTECT).contribute_to_class(AuthUserGroups, 'user')

    f = [f for f in UsersUserprofile._meta.local_fields if f.name != 'user_id']
    UsersUserprofile._meta.local_fields = f
    UsersUserprofile._meta.unique_together = []
    models.OneToOneField(AuthUser,
                         related_name='profile',
                         on_delete=models.PROTECT).contribute_to_class(UsersUserprofile, 'user')

    # Fix User ManyToManyField
    fld = models.ManyToManyField(AuthGroup,
                                 through=AuthUserGroups,
                                 ).contribute_to_class(AuthUser, 'groups')

    # Fix ReportsAppliedindicator ManyToManyField
    models.ManyToManyField(ReportsDisaggregation,
                           through=ReportsAppliedindicatorDisaggregation,
                           ).contribute_to_class(ReportsAppliedindicator, 'disaggregations')

    models.ManyToManyField(LocationsLocation,
                           through=ReportsAppliedindicatorLocations,
                           ).contribute_to_class(ReportsAppliedindicator, 'locations')

    # models.OneToOneField(UsersUserprofile,
    #                      on_delete=models.PROTECT,
    #                      ).contribute_to_class(AuthUser, 'profile')
    #

    # Fix UsersUserprofile ManyToManyField
    models.ManyToManyField(UsersCountry,
                           through=UsersUserprofileCountriesAvailable,
                           ).contribute_to_class(UsersUserprofile, 'countries_available')

    AuthUser.is_authenticated = True
    AuthUser.set_password = User.set_password

    # AuthUser.profile = cached_property(lambda self: UsersUserprofile.objects.get(user_id=self.id))

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

    # from django.apps import get_app, get_models

    app_models = apps.get_app_config('etools').get_models()
    for model in app_models:
        for attr in ['name', 'username']:
            if hasattr(model, attr):
                setattr(model, '__str__', partialmethod(partial(label, attr)))
                break

    aliases = (
        # CoreValuesAssessment.partner
        ['partnerspartnerorganization_partners_corevaluesassessment_partner_id',
         'core_values_assessments'],
        # PlannedEngagement
        # ['partnerspartnerorganization_partners_plannedengagement_partner_id',
        #  'planned_engagement'],
    )
    create_alias(PartnersPartnerorganization, aliases)

    f = [f for f in PartnersPlannedengagement._meta.local_fields if f.name != 'partner']
    PartnersPlannedengagement._meta.local_fields = f
    models.OneToOneField(PartnersPartnerorganization,
                         related_name='planned_engagement',
                         on_delete=models.PROTECT).contribute_to_class(PartnersPlannedengagement, 'partner')

    aliases = (['partnersintervention_partners_interventionbudget_intervention_id',
                'planned_budget'], ['partnersintervention_funds_fundsreservationheader_intervention_id',
                                    'frs'])
    create_alias(PartnersIntervention, aliases)

    T2FTravel.PLANNED = T2FTravel_PLANNED
    T2FTravel.SUBMITTED = T2FTravel_SUBMITTED
    T2FTravel.REJECTED = T2FTravel_REJECTED
    T2FTravel.APPROVED = T2FTravel_APPROVED
    T2FTravel.CANCELLED = T2FTravel_CANCELLED
    T2FTravel.SENT_FOR_PAYMENT = T2FTravel_SENT_FOR_PAYMENT
    T2FTravel.CERTIFICATION_SUBMITTED = T2FTravel_CERTIFICATION_SUBMITTED
    T2FTravel.CERTIFICATION_APPROVED = T2FTravel_CERTIFICATION_APPROVED
    T2FTravel.CERTIFICATION_REJECTED = T2FTravel_CERTIFICATION_REJECTED
    T2FTravel.CERTIFIED = T2FTravel_CERTIFIED
    T2FTravel.COMPLETED = T2FTravel_COMPLETED

    T2FTravel._meta.get_field('status').choices = T2FTravel_CHOICES
