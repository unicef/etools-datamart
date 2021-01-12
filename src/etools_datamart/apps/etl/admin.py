import json
from datetime import datetime

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import register
from django.contrib.postgres import fields
from django.core.cache import caches
from django.http import HttpResponseRedirect
from django.template import Context, Template
from django.template.defaultfilters import pluralize
from django.urls import NoReverseMatch, reverse
from django.utils import formats
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from admin_extra_urls.decorators import action
from admin_extra_urls.mixins import _confirm_action, ExtraUrlMixin
from adminactions.mass_update import mass_update
from django_celery_beat.models import PeriodicTask
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from unicef_rest_framework.models import Service

from etools_datamart.celery import app
from etools_datamart.libs.admin_filters import RangeFilter
from etools_datamart.libs.time import strfelapsed
from etools_datamart.sentry import process_exception

from . import models
from .loader import RUN_QUEUED, RUN_UNKNOWN

cache = caches['default']


def queue(modeladmin, request, queryset):
    count = len(queryset)
    for obj in queryset:
        modeladmin.queue(request, pk=obj.pk, message=False)
    modeladmin.message_user(request,
                            "{0} task{1} queued".format(count, pluralize(count)),
                            messages.SUCCESS)


def unlock(modeladmin, request, queryset):
    count = len(queryset)

    for obj in queryset:
        try:
            Service.objects.get_for_model(obj.loader.model).invalidate_cache()
        except Service.DoesNotExist:
            pass
        except Exception as e:
            process_exception(e)
        obj.loader.model.objects.truncate()
        obj.loader.unlock()

    modeladmin.message_user(request,
                            "{0} loader{1} unlocked".format(count, pluralize(count)),
                            messages.SUCCESS)


def truncate(modeladmin, request, queryset):
    count = len(queryset)

    for obj in queryset:
        try:
            Service.objects.get_for_model(obj.loader.model).invalidate_cache()
        except Service.DoesNotExist:
            pass
        except Exception as e:
            process_exception(e)
        obj.loader.model.objects.truncate()
        obj.loader.unlock()
        obj.status = 'NO DATA'
        obj.last_run = None
        obj.run_type = RUN_UNKNOWN
        obj.last_success = None
        obj.last_failure = None
        obj.time = None
        obj.save()
    modeladmin.message_user(request,
                            "{0} table{1} truncated".format(count, pluralize(count)),
                            messages.SUCCESS)


def get_css(obj):
    css = ''
    if obj.status:
        if obj.status in ['QUEUED']:
            pass
        elif obj.status in ['RUNNING', 'STARTED']:
            css = 'run'
        elif obj.status in ['FAILURE', 'ERROR', 'NO DATA']:
            css = 'error'
        elif 'RETRY' in obj.status:
            css = 'warn'
        elif obj.last_failure:
            css = 'error'
        elif obj.last_run and (obj.last_run.date() < datetime.today().date()):
            css = 'warn'
        elif obj.status == 'SUCCESS':
            css = 'success'
    return css


def df(value):
    # formats.date_format(obj.last_success, 'DATETIME_FORMAT')
    if value is not None:
        return value.strftime("%b %d, %H:%M")
        # dateformat.format(value, 'b d, H:i')


class JSONROWidget(forms.Textarea):
    tpl = '''<input type="hidden" name="{{ widget.name }}"{% if widget.value != None %} value="{{ widget.value|stringformat:'s' }}"{% endif %}>
    {{style}}{{json}}'''

    def render(self, name, value, attrs=None, renderer=None):
        formatter = HtmlFormatter(style='colorful')
        formatted_json = highlight(json.dumps(json.loads(value), sort_keys=True, indent=2),
                                   JsonLexer(), formatter)

        context = self.get_context(name, value, attrs)
        context['json'] = mark_safe(formatted_json)
        context['style'] = mark_safe("<style>" + formatter.get_style_defs() + "</style>")
        template = Template(self.tpl)
        return template.render(Context(context))

        # style =
        # return mark_safe(original + style + response)
        # return mark_safe(json.dumps(value, sort_keys=True, indent=4))


@register(models.EtlTask)
class EtlTaskAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('task', '_last_run', '_status',
                    '_total', 'time',
                    '_last_success', '_last_failure',
                    'unlock_task', 'queue_task', 'data'
                    )

    date_hierarchy = 'last_run'
    actions = [mass_update, queue, truncate, unlock]
    mass_update_hints = ['status', ]
    mass_update_exclude = ['task', 'table_name', 'content_type']
    # readonly_fields = ['results', ]
    formfield_overrides = {
        fields.JSONField: {'widget': JSONROWidget},
    }

    def _total(self, obj):
        try:
            a = obj.results.get('processed', '-')
            b = obj.results.get('total_records', '-')
            return "%s/%s" % (a, b)
        except Exception:
            return '?'

    def _task_id(self, obj):
        return (obj.task_id or '')[:8]

    def _last_run(self, obj):
        if obj.last_run:
            dt = df(obj.last_run)
            css = get_css(obj)
            return mark_safe('<span class="%s">%s</span>' % (css, dt))

    _last_run.admin_order_field = 'last_run'

    def _last_success(self, obj):
        if obj.last_success:
            dt = df(obj.last_success)
            css = get_css(obj)
            return mark_safe('<span class="%s">%s</span>' % (css, dt))

    _last_success.admin_order_field = 'last_success'

    def _last_failure(self, obj):
        if obj.last_failure:
            dt = formats.date_format(obj.last_failure, 'DATE_FORMAT')
            css = get_css(obj)
            return mark_safe('<span class="%s">%s</span>' % (css, dt))

    _last_failure.admin_order_field = 'last_failure'

    def _status(self, obj):
        css = get_css(obj)
        if obj.status and 'RETRY' in obj.status:
            s = '%s</br>%s' % (obj.status, obj.results)
        else:
            c = cache.get("STATUS:%s" % obj.task) or ""
            s = obj.status
            if c:
                s = "%s (%s)" % (obj.status, c)
        return mark_safe('<span class="%s">%s</span>' % (css, s))

    _status.verbose_name = 'status'
    _status.admin_order_field = 'status'

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
        model = obj.loader.model
        opts = model._meta
        try:
            url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))
            return format_html(f'<a href="{url}">data</a>')
        except NoReverseMatch:
            return '-'

    def queue_task(self, obj):
        opts = self.model._meta
        url = reverse('admin:%s_%s_queue' % (opts.app_label,
                                             opts.model_name), args=[obj.id])
        return format_html(f'<a href="{url}">queue</a>')

    queue_task.verbose_name = 'queue'

    def unlock_task(self, obj):
        if obj.content_type:
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
    def check_running(self, request, message=True):
        # {'celery@gundam.local': [{'id': '7a570647-89cd-4c47-84e4-c8569ef48f28',
        #                           'name': 'load_data_hact',
        #                           'args': '()',
        #                           'kwargs': '{}',
        #                           'type': 'load_data_hact',
        #                           'hostname': 'celery@gundam.local',
        #                           'time_start': 1567185669.1479037,
        #                           'acknowledged': True,
        #                           'delivery_info': {'exchange': '',
        #                                             'routing_key': 'default',
        #                                             'priority': 0,
        #                                             'redelivered': None},
        #                           'worker_pid': 40223}]}
        from etools_datamart.celery import app
        i = app.control.inspect()
        s = i.stats()
        if not s:
            self.message_user(request, "Warning unable to get celery control", messages.ERROR)
        running = i.active()
        founds = []
        if running:
            for worker, tasks in running.items():
                for task in tasks:
                    founds.append(task['name'])
                    models.EtlTask.objects.filter(task=task['name']).update(task_id=task['id'])
        models.EtlTask.objects.exclude(task__in=founds).update(task_id=None)

    @action()
    def queue(self, request, pk, message=True):
        obj = self.get_object(request, pk)
        try:
            obj.status = 'QUEUED'
            obj.elapsed = None
            obj.save()
            task = app.tasks.get(obj.task)
            task.delay(run_type=RUN_QUEUED)
            if message:
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

    @action()
    def inspect(self, request):
        created, updated = self.model.objects.inspect()
        self.message_user(request, f"{created} task created. {updated} have been updated",
                          messages.SUCCESS)


class ElapsedFilter(RangeFilter):
    title = 'Elapsed'
    parameter_name = 'elapsed'

    ranges = {1: ('< 1m', dict(elapsed__lt=60)),
              2: ('> 1m', dict(elapsed__gt=60)),
              3: ('> 10m', dict(elapsed__gt=60 * 10)),
              4: ('> 1h', dict(elapsed__gt=60 * 60)),
              }


class DeltaFilter(RangeFilter):
    title = 'Delta'
    parameter_name = 'delta'

    ranges = {1: ('< 10%', dict(delta_percentage__lt=10)),
              2: ('> 10%', dict(delta_percentage__gt=10)),
              3: ('> 20%', dict(delta_percentage__gt=20)),
              4: ('> 50%', dict(delta_percentage__gt=50))
              }


@register(models.EtlTaskHistory)
class EtlTaskHistoryAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('task', 'timestamp', 'time', 'incr')
    list_filter = ('task', ElapsedFilter, DeltaFilter)
    actions = [mass_update]
    mass_update_fields = ('delta', 'delta_percentage')
    mass_update_exclude = None
    date_hierarchy = 'timestamp'
    search_fields = ('task',)

    def incr(self, obj):
        if obj.delta_percentage:
            return "{0:.2f}%".format(obj.delta_percentage)

    def time(self, obj):
        return strfelapsed(obj.elapsed)

    time.admin_order_field = 'elapsed'

    @action()
    def delta(self, request):
        qs = self.get_queryset(request).order_by('-timestamp')
        for e in qs.filter(delta__isnull=True):
            prev = qs.filter(task=e.task,
                             timestamp__lt=e.timestamp).exclude(id=e.id).first()
            if prev:
                e.delta = e.elapsed - prev.elapsed
                try:
                    # e.delta_percentage = (100.0 * (e.elapsed / prev.elapsed)) - 100
                    # 1 / 2 * 100
                    if prev.elapsed:
                        e.delta_percentage = (e.elapsed / prev.elapsed) * 100
                except ZeroDivisionError:
                    pass
            else:
                e.delta = None
            e.save()
