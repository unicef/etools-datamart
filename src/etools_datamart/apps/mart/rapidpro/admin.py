from django.contrib.admin import ModelAdmin, register

from admin_extra_buttons.mixins import ExtraButtonsMixin

from etools_datamart.apps.core.admin_mixins import ReadOnlyMixin
from etools_datamart.apps.mart.data.admin import DataModelAdmin

from . import models


class RapidProAdmin(ReadOnlyMixin, DataModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return []

    def get_list_filter(self, request):
        # if 'last_modify_date' not in self.list_filter:
        #     self.list_filter = self.list_filter + ('last_modify_date',)
        return self.list_filter


@register(models.Source)
class SourceAdmin(ExtraButtonsMixin, ModelAdmin):
    list_display = ("name", "server", "is_active")
    list_filter = ("is_active",)


@register(models.Organization)
class OrganizationAdmin(RapidProAdmin):
    list_filter = ()


@register(models.Group)
class GroupAdmin(RapidProAdmin):
    list_display = ("id", "organization", "name", "query", "count")
    list_filter = ("organization",)
    search_fields = ("name",)


@register(models.Contact)
class ContactAdmin(RapidProAdmin):
    list_display = ("id", "organization", "name", "language", "blocked", "stopped")
    list_filter = ("organization",)
    search_fields = ("name",)


@register(models.Label)
class LabelAdmin(RapidProAdmin):
    list_display = (
        "id",
        "uuid",
        "name",
        "count",
    )
    list_filter = ("organization",)
    search_fields = ("name",)


@register(models.Runs)
class RunsAdmin(RapidProAdmin):
    list_display = (
        "id",
        "flow",
        "active",
        "completed",
        "expired",
        "interrupted",
    )
    list_filter = ("organization",)


@register(models.Flow)
class FlowAdmin(RapidProAdmin):
    list_display = ("id", "name", "archived", "expires", "runs")
    list_filter = ("organization",)
    search_fields = ("name",)


@register(models.FlowStart)
class FlowStartAdmin(RapidProAdmin):
    list_display = ("id", "uuid", "flow", "status", "created_on")
    list_filter = ("organization",)
    raw_id_fields = ("flow", "organization")
    exclude = ("groups", "contacts")
