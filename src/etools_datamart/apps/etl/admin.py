# -*- coding: utf-8 -*-
from admin_extra_urls.extras import action, link
from admin_extra_urls.mixins import _confirm_action
from django.contrib import admin, messages
from django.contrib.admin import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django_celery_beat.models import PeriodicTask
from humanize import naturaldelta

from etools_datamart.apps.etl.lock import cache
from etools_datamart.celery import app
from etools_datamart.libs.truncate import TruncateTableMixin

from . import models


@register(models.EtlTask)
class EtlTaskAdmin(TruncateTableMixin, admin.ModelAdmin):
    list_display = ('task', 'timestamp', 'result', 'time',
                    'last_success', 'last_failure', 'lock', 'scheduling', 'queue_task')

    readonly_fields = ('task', 'timestamp', 'result', 'elapsed', 'time',
                       'last_success', 'last_failure', 'table_name', 'content_type')
    date_hierarchy = 'timestamp'
    actions = None

    def scheduling(self, obj):
        opts = PeriodicTask._meta
        if obj.periodic_task:
            pt = obj.periodic_task
            url = reverse('admin:%s_%s_change' % (opts.app_label,
                                                  opts.model_name), args=[pt.id])
            url = f"{url}?name={obj.task}&task={obj.task}"
            label = (pt.crontab or pt.solar or pt.interval)
        else:
            url = reverse('admin:%s_%s_add' % (opts.app_label, opts.model_name))
            label = 'Schedule'

        return format_html(f'<a href="{url}">{label}</a>')

    def queue_task(self, obj):
        opts = self.model._meta
        url = reverse('admin:%s_%s_queue' % (opts.app_label,
                                             opts.model_name), args=[obj.id])
        return format_html(f'<a href="{url}">queue</a>')
    queue_task.verbse_name = 'queue'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def time(self, obj):
        return naturaldelta(obj.elapsed)

    def lock(self, obj):
        return f"{obj.task}-lock" in cache

    lock.boolean = True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)

    @action()
    def queue(self, request, pk):
        obj = self.get_object(request, pk)
        try:
            task = app.tasks[obj.task]
            task.delay()
            self.message_user(request, f"Task '{obj.task}' queued", messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            self.message_user(request, f"Cannot queue '{obj.task}': {e}", messages.ERROR)

    @action(visible=lambda obj: f"{obj.task}-lock" in cache)
    def unlock(self, request, pk):
        obj = self.get_object(request, pk)
        key = f"{obj.task}-lock"

        def _action(request):
            cache.delete(key)

        return _confirm_action(self, request, _action, f"Continuing will unlock selected task. ({key})",
                               "Successfully executed", )

    @link()
    def inspect(self, request):
        created, updated = self.model.objects.inspect()
        self.message_user(request, f"{created} task created. {updated} have been updated",
                          messages.SUCCESS)
