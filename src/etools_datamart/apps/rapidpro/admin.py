from django.contrib.admin import ModelAdmin, register

from admin_extra_urls.extras import ExtraUrlMixin

from etools_datamart.apps.core.admin_mixins import ReadOnlyMixin
from etools_datamart.apps.data.admin import DataModelAdmin

from . import models


class RapidProAdmin(ReadOnlyMixin, DataModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return []

    def get_list_filter(self, request):
        # if 'last_modify_date' not in self.list_filter:
        #     self.list_filter = self.list_filter + ('last_modify_date',)
        return self.list_filter


@register(models.Source)
class SourceAdmin(ExtraUrlMixin, ModelAdmin):
    list_display = ('name', 'server', 'is_active')
    list_filter = ('is_active',)


@register(models.Organization)
class OrganizationAdmin(RapidProAdmin):
    list_filter = ()


@register(models.Group)
class GroupAdmin(RapidProAdmin):
    list_display = ('id', 'organization', 'name', 'query', 'count')
    list_filter = ('organization',)
    search_fields = ('name',)


@register(models.Contact)
class ContactAdmin(RapidProAdmin):
    list_display = ('id', 'organization', 'name', 'language', 'blocked', 'stopped')
    list_filter = ('organization',)
    search_fields = ('name',)
