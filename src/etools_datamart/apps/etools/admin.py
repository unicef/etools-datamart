# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, register

from . import models


@register(models.ActionPointsActionpoint)
class ActionPoint(ModelAdmin):
    pass


@register(models.ActivitiesActivity)
class ActivitiesActivity(ModelAdmin):
    pass


@register(models.PartnersPartnerorganization)
class PartnersPartnerorganization(ModelAdmin):
    list_display = ('vendor_number', 'partner_type', 'name', 'short_name')
    search_fields = ('name', )
    list_filter = ('country',)


@register(models.PartnersAssessment)
class PartnersAssessment(ModelAdmin):
    pass


@register(models.PartnersAgreement)
class PartnersAgreement(ModelAdmin):
    pass


@register(models.AuditEngagement)
class AuditEngagement(ModelAdmin):
    pass
