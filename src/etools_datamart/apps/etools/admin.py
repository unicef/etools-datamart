# -*- coding: utf-8 -*-
from django.contrib.admin import register

from etools_datamart.apps.multitenant.admin import TenantModelAdmin

from . import models


@register(models.ActionPointsActionpoint)
class ActionPoint(TenantModelAdmin):
    pass


@register(models.ActivitiesActivity)
class ActivitiesActivity(TenantModelAdmin):
    pass


@register(models.PartnersPartnerorganization)
class PartnersPartnerorganization(TenantModelAdmin):
    list_display = ('vendor_number', 'partner_type', 'name', 'short_name', 'schema')
    search_fields = ('name',)
    # list_filter = ('schema',)


@register(models.PartnersAssessment)
class PartnersAssessment(TenantModelAdmin):
    pass


@register(models.PartnersAgreement)
class PartnersAgreement(TenantModelAdmin):
    pass


@register(models.AuditEngagement)
class AuditEngagement(TenantModelAdmin):
    pass


@register(models.PartnersIntervention)
class PartnersIntervention(TenantModelAdmin):
    pass


@register(models.T2FTravel)
class T2FTravel(TenantModelAdmin):
    pass


@register(models.ReportsAppliedindicator)
class ReportsAppliedindicator(TenantModelAdmin):
    pass


@register(models.ReportsResult)
class ReportsResult(TenantModelAdmin):
    list_display = ('name', 'code', 'result_type',)


@register(models.ReportsResulttype)
class ReportsResulttype(TenantModelAdmin):
    list_display = ('id', 'name', 'schema')
