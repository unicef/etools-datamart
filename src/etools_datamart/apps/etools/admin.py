# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, register, helpers
from django.utils.safestring import mark_safe

from . import models

from django.contrib.admin.views.main import ChangeList


class TenantChangeList(ChangeList):
    pass


class TenantModelAdmin(ModelAdmin):
    actions = None

    def get_object(self, request, object_id, from_field=None):
        return super().get_object(request, object_id, from_field)

    def get_changelist(self, request, **kwargs):
        """
        Return the ChangeList class for use on the changelist page.
        """
        return ChangeList

    def get_changelist_instance(self, request):
        """
        Return a `ChangeList` instance based on `request`. May raise
        `IncorrectLookupParameters`.
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        if self.get_actions(request):
            list_display = ['action_checkbox'] + list(list_display)
        _ChangeList = self.get_changelist(request)
        return _ChangeList(
            request,
            self.model,
            list_display,
            list_display_links,
            self.get_list_filter(request),
            self.date_hierarchy,
            self.get_search_fields(request),
            self.get_list_select_related(request),
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
        )


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
