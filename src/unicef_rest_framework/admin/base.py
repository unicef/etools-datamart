# -*- coding: utf-8 -*-

import logging

from admin_extra_urls.extras import link
from admin_extra_urls.mixins import _confirm_action
from django.contrib import admin

logger = logging.getLogger(__name__)


class ReadOnlyModelAdmin(object):
    editing = False

    def get_readonly_fields(self, request, obj=None):
        if self.editing:
            return self.readonly_fields
        return [f.name for f in self.model._meta.fields]


class TruncateTableMixin:

    def _truncate(self, request):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE {0}'.format(self.model._meta.db_table))

    @link(label='Truncate', css_class="btn btn-danger", permission=lambda request, obj: request.user.is_superuser)
    def truncate(self, request):
        return _confirm_action(self, request, self._truncate, "Continuing will erase the entire content of the table.",
                               "Successfully executed", )


class ListDisplayAllMixin(object):
    list_display = ()
    list_display_exclude = ('id', 'uuid', 'version',
                            'last_modified_user', 'last_modified_date')

    def get_list_display(self, request):
        if not self.list_display:
            return [f.name for f in self.model._meta.fields
                    if f.name not in self.list_display_exclude]
        return self.list_display


class APIModelAdmin(ListDisplayAllMixin, ReadOnlyModelAdmin,
                    admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

        # def has_change_permission(self, request, obj=None):
        # return obj is None
