# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin, messages
from django.contrib.admin import register
from django.http import HttpResponseRedirect
from django.template.defaultfilters import pluralize
from django.urls import reverse
from django.utils import formats
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from admin_extra_urls.extras import action, ExtraUrlMixin, link
from admin_extra_urls.mixins import _confirm_action
from adminactions.mass_update import mass_update
from crashlog.middleware import process_exception
from django_celery_beat.models import PeriodicTask

from etools_datamart.apps.data.loader import RUN_QUEUED
from etools_datamart.celery import app
from etools_datamart.libs.time import strfelapsed

from . import models


def queue(modeladmin, request, queryset):
    count = len(queryset)
    for obj in queryset:
        modeladmin.queue(request, obj.pk)
        # task = app.tasks.get(obj.task)
        # task.delay(run_type=RUN_QUEUED)
    modeladmin.message_user(request,
                            "{0} task{1} queued".format(count, pluralize(count)),
                            messages.SUCCESS)


def force(modeladmin, request, queryset):
    count = len(queryset)
    for obj in queryset:
        task = app.tasks.get(obj.task)
        task.delay(run_type=RUN_QUEUED, ignore_dependencies=True)
    modeladmin.message_user(request,
                            "{0} task{1} forced".format(count, pluralize(count)),
                            messages.SUCCESS)


def get_css(obj):
    css = ''
    if obj.status in ['FAILURE', 'ERROR']:
        css = 'error'
    elif obj.last_failure:
        css = 'error'
    elif obj.last_run.date() < datetime.today().date():
        css = 'warn'
    elif obj.status == 'SUCCESS':
        css = 'success'
    return css


@register(models.EtlTask)
class EtlTaskAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('task', '_last_run', 'run_type', '_status', 'time',
                    '_last_success', 'last_failure',
                    'crontab', 'unlock_task', 'queue_task'
                    )

    date_hierarchy = 'last_run'
    actions = [mass_update, queue, force]

    def _last_run(self, obj):
        if obj.last_run:
            dt = formats.date_format(obj.last_run, 'DATETIME_FORMAT')
            css = get_css(obj)
            return mark_safe('<span class="%s">%s</span>' % (css, dt))

    def _last_success(self, obj):
        if obj.last_success:
            dt = formats.date_format(obj.last_success, 'DATETIME_FORMAT')
            css = get_css(obj)
            return mark_safe('<span class="%s">%s</span>' % (css, dt))

    def _last_failure(self, obj):
        if obj.last_failure:
            dt = formats.date_format(obj.last_failure, 'DATE_FORMAT')
            css = get_css(obj)
            return mark_safe('<span class="%s">%s</span>' % (css, dt))

    def _status(self, obj):
        css = get_css(obj)
        return mark_safe('<span class="%s">%s</span>' % (css, obj.status))

    _status.verbse_name = 'status'

    def crontab(self, obj):
        opts = PeriodicTask._meta
        label = 'cron'

        if obj.periodic_task:
            pt = obj.periodic_task
            url = reverse('admin:%s_%s_change' % (opts.app_label,
                                                  opts.model_name), args=[pt.id])
            url = f"{url}?name={obj.task}&task={obj.task}"
            # label = (pt.crontab or pt.solar or pt.interval)
        else:
            url = reverse('admin:%s_%s_add' % (opts.app_label, opts.model_name))

        return format_html(f'<a href="{url}">{label}</a>')

    def data(self, obj):
        model = obj.content_type.model_class()
        opts = model._meta
        url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))
        return format_html(f'<a href="{url}">data</a>')

    data.verbse_name = 'data'

    def queue_task(self, obj):
        opts = self.model._meta
        url = reverse('admin:%s_%s_queue' % (opts.app_label,
                                             opts.model_name), args=[obj.id])
        return format_html(f'<a href="{url}">queue</a>')

    queue_task.verbose_name = 'queue'

    def unlock_task(self, obj):
        locked = obj.content_type.model_class().loader.is_locked
        if locked:
            css = 'error'
            label = 'unlock'
        else:
            css = 'success'
            label = 'force unlock'

        opts = self.model._meta
        url = reverse('admin:%s_%s_unlock' % (opts.app_label,
                                              opts.model_name), args=[obj.id])
        return format_html(f'<a href="{url}"><span class="{css}">{label}</span></a>')

    unlock_task.verbose_name = 'unlock'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def time(self, obj):
        return strfelapsed(obj.elapsed)

    time.admin_order_field = 'elapsed'

    # def locked(self, obj):
    #     try:
    #         return obj.content_type.model_class().loader.is_locked
    #     except Exception as e:
    #         return 'Error: %s' % e

    # locked.boolean = True
    #
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if request.method == 'POST':
    #         redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
    #                                                            self.opts.model_name))
    #         return HttpResponseRedirect(redirect_url)
    #     return self._changeform_view(request, object_id, form_url, extra_context)

    @action()
    def queue(self, request, pk):
        obj = self.get_object(request, pk)
        try:
            obj.status = 'QUEUED'
            obj.elapsed = None
            obj.save()
            task = app.tasks.get(obj.task)
            task.delay(run_type=RUN_QUEUED)
            self.message_user(request, f"Task '{obj.task}' queued", messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            process_exception(e)
            self.message_user(request, f"Cannot queue '{obj.task}': {e}", messages.ERROR)
        return HttpResponseRedirect(reverse("admin:etl_etltask_changelist"))

    @action()
    def unlock(self, request, pk):

        obj = self.get_object(request, pk)

        def _action(request):
            obj.loader.unlock()

        return _confirm_action(self, request, _action,
                               f"""Continuing will unlock selected task. ({obj.task}).
{obj.loader.task.name} - {obj.loader.config.lock_key}
""",
                               "Successfully executed", )

    @link()
    def inspect(self, request):
        created, updated = self.model.objects.inspect()
        self.message_user(request, f"{created} task created. {updated} have been updated",
                          messages.SUCCESS)
