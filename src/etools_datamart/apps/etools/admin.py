# -*- coding: utf-8 -*-
from django.contrib.admin import register

from etools_datamart.apps.multitenant.admin import TenantModelAdmin

from . import models


@register(models.ActionPointsActionpoint)
class ActionPoint(TenantModelAdmin):
    pass


@register(models.ActivitiesActivity)
class ActivitiesActivityAdmin(TenantModelAdmin):
    pass


@register(models.PartnersPartnerorganization)
class PartnerOrganizationAdmin(TenantModelAdmin):
    list_display = ('vendor_number', 'partner_type', 'name', 'short_name', 'schema')
    search_fields = ('name',)
    # list_filter = ('schema',)


@register(models.PartnersAssessment)
class PartnersAssessmentAdmin(TenantModelAdmin):
    pass


@register(models.PartnersAgreement)
class PartnersAgreementAdmin(TenantModelAdmin):
    search_fields = ('partner__name',)
    list_display = ('agreement_number', 'agreement_type', 'partner', 'schema')
    # list_filter = ('agreement_type', )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('partner')


@register(models.AuditEngagement)
class AuditEngagementAdmin(TenantModelAdmin):
    pass


@register(models.PartnersIntervention)
class PartnersInterventionAdmin(TenantModelAdmin):
    list_display = ('number', 'title', 'document_type', 'schema')
    list_filter = ('document_type',)


@register(models.T2FTravel)
class T2FTravelAdmin(TenantModelAdmin):
    pass


@register(models.ReportsAppliedindicator)
class ReportsAppliedindicatorAdmin(TenantModelAdmin):
    pass


@register(models.ReportsResult)
class ReportsResultAdmin(TenantModelAdmin):
    list_display = ('name', 'code', 'result_type',)


@register(models.ReportsResulttype)
class ReportsResulttypeAdmin(TenantModelAdmin):
    list_display = ('id', 'name', 'schema')


@register(models.PartnersPlannedengagement)
class PartnersPlannedEngagementAdmin(TenantModelAdmin):
    pass


@register(models.FundsFundsreservationheader)
class FundsReservationHeaderAdmin(TenantModelAdmin):
    pass


@register(models.FundsFundsreservationitem)
class FundsreservationitemAdmin(TenantModelAdmin):
    pass
