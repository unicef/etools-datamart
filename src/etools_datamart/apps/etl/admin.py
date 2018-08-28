# -*- coding: utf-8 -*-
from admin_extra_urls.extras import action, ExtraUrlMixin, link
from admin_extra_urls.mixins import _confirm_action
from django.contrib import admin
from django.contrib.admin import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from humanize import naturaldelta

from etools_datamart.apps.etl.lock import cache

from . import models


@register(models.Execution)
class ExecutionAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('task', 'timestamp', 'result', 'time',
                    'last_success', 'last_failure', 'running')
    readonly_fields = ('task', 'timestamp', 'result', 'elapsed', 'time',
                       'last_success', 'last_failure')
    date_hierarchy = 'timestamp'
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def time(self, obj):
        return naturaldelta(obj.elapsed)

    def running(self, obj):
        return f"{obj.task}-lock" in cache

    running.boolean = True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)

    @action()
    def unlock(self, request, pk):
        obj = self.get_object(request, pk)
        key = f"{obj.task}-lock"

        def _action(request):
            cache.delete(key)

        return _confirm_action(self, request, _action, f"Continuing will unlock selected task. ({key})",
                               "Successfully executed", )

    @link()
    def truncate(self, request):
        def _action(request):
            from django.db import connection

            cursor = connection.cursor()
            cursor.execute('TRUNCATE TABLE {0}'.format(self.model._meta.db_table))

        return _confirm_action(self, request, _action, "Continuing will erase the entire content of the table.",
                               "Successfully executed", )
