import logging

from django.contrib import admin

from admin_extra_urls.decorators import action
from admin_extra_urls.mixins import _confirm_action, ExtraUrlMixin

logger = logging.getLogger(__name__)


class ReadOnlyAdminMixin:
    editing = False

    def get_readonly_fields(self, request, obj=None):
        if self.editing:
            return self.readonly_fields
        return [f.name for f in self.model._meta.fields]


class TruncateTableMixin(ExtraUrlMixin):

    def _truncate(self, request):
        self.model.objects.truncate()

    @action(label='Truncate', permission=lambda request, obj: request.user.is_superuser)
    def truncate(self, request):
        return _confirm_action(self, request, self._truncate, "Continuing will erase the entire content of the table.",
                               "Successfully executed", )


class ListDisplayAllMixin:
    list_display = ()
    list_display_exclude = ('id', 'uuid', 'version',
                            'last_modified_user', 'last_modified_date')

    def get_list_display(self, request):
        if not self.list_display:
            return [f.name for f in self.model._meta.fields
                    if f.name not in self.list_display_exclude]
        return self.list_display


class APIModelAdmin(ListDisplayAllMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    # return obj is None
