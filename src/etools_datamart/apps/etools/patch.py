# -*- coding: utf-8 -*-
# flake8: noqa F405
from functools import partial, partialmethod

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

from unicef_security.models import User

from etools_datamart.apps.etools.models import PartnersPlannedengagement, T2FTravel, ReportsAppliedindicator, \
    ReportsAppliedindicatorDisaggregation, ReportsAppliedindicatorLocations, ReportsDisaggregation, LocationsLocation


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

    T2FTravel.PLANNED = 'planned'
    T2FTravel.SUBMITTED = 'submitted'
    T2FTravel.REJECTED = 'rejected'
    T2FTravel.APPROVED = 'approved'
    T2FTravel.CANCELLED = 'cancelled'
    T2FTravel.SENT_FOR_PAYMENT = 'sent_for_payment'
    T2FTravel.CERTIFICATION_SUBMITTED = 'certification_submitted'
    T2FTravel.CERTIFICATION_APPROVED = 'certification_approved'
    T2FTravel.CERTIFICATION_REJECTED = 'certification_rejected'
    T2FTravel.CERTIFIED = 'certified'
    T2FTravel.COMPLETED = 'completed'

    T2FTravel.CHOICES = (
        (T2FTravel.PLANNED, _('Planned')),
        (T2FTravel.SUBMITTED, _('Submitted')),
        (T2FTravel.REJECTED, _('Rejected')),
        (T2FTravel.APPROVED, _('Approved')),
        (T2FTravel.COMPLETED, _('Completed')),
        (T2FTravel.CANCELLED, _('Cancelled')),
        (T2FTravel.SENT_FOR_PAYMENT, _('Sent for payment')),
        (T2FTravel.CERTIFICATION_SUBMITTED, _('Certification submitted')),
        (T2FTravel.CERTIFICATION_APPROVED, _('Certification approved')),
        (T2FTravel.CERTIFICATION_REJECTED, _('Certification rejected')),
        (T2FTravel.CERTIFIED, _('Certified')),
        (T2FTravel.COMPLETED, _('Completed')),
    )
    T2FTravel._meta.get_field('status').choices = T2FTravel.CHOICES
