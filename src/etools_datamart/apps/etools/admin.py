# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, register, helpers
from django.utils.safestring import mark_safe

from . import models


class TenantModelAdmin(ModelAdmin):
    # def action_checkbox(self, obj):
    #     """
    #     A list_display column containing a checkbox widget.
    #     """
    #     return helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, str(obj.pk))
    # action_checkbox.short_description = mark_safe('<input type="checkbox" id="action-toggle" />')
    pass

@register(models.ActionPointsActionpoint)
class ActionPoint(TenantModelAdmin):
    pass


@register(models.ActivitiesActivity)
class ActivitiesActivity(TenantModelAdmin):
    pass


@register(models.PartnersPartnerorganization)
class PartnersPartnerorganization(TenantModelAdmin):
    list_display = ('vendor_number', 'partner_type', 'name', 'short_name')
    search_fields = ('name',)
    list_filter = ('country',)


@register(models.PartnersAssessment)
class PartnersAssessment(TenantModelAdmin):
    pass


@register(models.PartnersAgreement)
class PartnersAgreement(TenantModelAdmin):
    pass


@register(models.AuditEngagement)
class AuditEngagement(TenantModelAdmin):
    pass
