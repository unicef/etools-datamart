from django.utils.translation import ugettext_lazy as _

from admin_extra_urls.extras import action, ExtraUrlMixin
from adminactions.mass_update import mass_update, MassUpdateForm
from django_celery_beat import admin
from kombu.utils.json import loads

from unicef_rest_framework.models import PeriodicTask


class PeriodicTaskUpdateForm(MassUpdateForm):
    class Meta:
        fields = ('interval', 'crontab', 'solar', 'queue', 'exchange', 'routing_key',
                  'priority', 'expires', 'one_off', 'enabled',)


class PeriodicTaskAdmin(ExtraUrlMixin, admin.PeriodicTaskAdmin):
    list_display = ('name', 'service', 'enabled', 'schedule', 'one_off', 'total_run_count')
    list_filter = ('enabled', 'last_run_at', 'service')
    date_hierarchy = 'last_run_at'
    actions = ('enable_tasks', 'disable_tasks', 'toggle_tasks', 'run_tasks', mass_update)
    mass_update_form = PeriodicTaskUpdateForm
    fieldsets = (
        (None, {
            'fields': (('name', 'service'), ('regtask', 'task'), 'enabled', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab', 'solar',
                       'start_time', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Arguments', {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
        ('Execution Options', {
            'fields': ('expires', 'queue', 'exchange', 'routing_key'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
    )

    @action()
    def run_task(self, request, pk):
        periodic_task = PeriodicTask.objects.get(pk=pk)
        self.celery_app.loader.import_default_modules()

        task = self.celery_app.tasks.get(periodic_task.task)
        task.delay(*loads(periodic_task.args), **loads(periodic_task.kwargs))

        self.message_user(request, _('task successfully run'))

    def schedule(self, obj):
        fmt = '{{no schedule}}'
        if obj.interval:
            fmt = '{0.interval}'
        elif obj.crontab:
            fmt = '{0.crontab}'
        elif obj.solar:
            fmt = '{0.solar}'
        return fmt.format(obj)


class CrontabScheduleAdmin(admin.admin.ModelAdmin):
    list_display = ('minute', 'hour', 'day_of_month', 'month_of_year')
