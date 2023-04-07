from urllib.parse import quote

from django import forms
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import quote
from django.http import HttpResponseRedirect
from django.template.defaultfilters import pluralize
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin
from adminactions.mass_update import mass_update, MassUpdateForm
from django_celery_beat import admin
from django_celery_beat.admin import PeriodicTaskForm
from kombu.utils.json import loads

from unicef_rest_framework.models import PeriodicTask


class PeriodicTaskUpdateForm(MassUpdateForm):
    class Meta:
        fields = (
            "interval",
            "crontab",
            "solar",
            "queue",
            "exchange",
            "routing_key",
            "priority",
            "expires",
            "one_off",
            "enabled",
        )


class PeriodicTaskPreloadForm(PeriodicTaskForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"style": "width:500px"}))
    args = forms.CharField(widget=forms.TextInput(attrs={"style": "width:500px"}))
    task = forms.CharField(widget=forms.TextInput(attrs={"style": "width:400px"}))

    class Meta:
        model = PeriodicTask
        fields = ("name", "task", "service", "enabled", "crontab", "args", "kwargs")
        widgets = {"kwargs": forms.HiddenInput}


class PeriodicTaskAdmin(ExtraButtonsMixin, admin.PeriodicTaskAdmin):
    list_display = ("name", "enabled", "schedule", "one_off", "total_run_count")
    list_filter = (
        "enabled",
        "last_run_at",
    )
    date_hierarchy = "last_run_at"
    search_fields = ("service__name", "name")
    actions = ("enable_tasks", "disable_tasks", "toggle_tasks", "run_tasks", mass_update)
    mass_update_form = PeriodicTaskUpdateForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "service"),
                    ("regtask", "task"),
                    "enabled",
                    "description",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Schedule",
            {
                "fields": ("interval", "crontab", "solar", "start_time", "one_off"),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Arguments",
            {
                "fields": ("args", "kwargs"),
                "classes": ("extrapretty", "wide", "collapse", "in"),
            },
        ),
        (
            "Execution Options",
            {
                "fields": ("expires", "queue", "exchange", "routing_key"),
                "classes": ("extrapretty", "wide", "collapse", "in"),
            },
        ),
    )

    def run_tasks(self, request, queryset):
        self.celery_app.loader.import_default_modules()
        tasks = [
            (self.celery_app.tasks.get(periodic_task.task), loads(periodic_task.args), loads(periodic_task.kwargs))
            for periodic_task in queryset
        ]

        task_ids = [task.delay(*args, **kwargs) for task, args, kwargs in tasks if task and task.delay]

        tasks_run = len(task_ids)
        self.message_user(
            request,
            _("{0} task{1} {2} successfully run").format(
                tasks_run,
                pluralize(tasks_run),
                pluralize(tasks_run, _("was,were")),
            ),
        )

    run_tasks.short_description = _("Run selected tasks")

    @button()
    def queue_task(self, request, pk):
        periodic_task = PeriodicTask.objects.get(pk=pk)
        self.celery_app.loader.import_default_modules()

        task = self.celery_app.tasks.get(periodic_task.task)
        task.delay(*loads(periodic_task.args), **loads(periodic_task.kwargs))

        self.message_user(request, _("task successfully queued"))

    @button()
    def preload(self, request):
        opts = self.model._meta
        app_label = opts.app_label
        _from = request.GET.get("_from", ".")
        name = request.GET.get("name", None)
        obj = PeriodicTask.objects.filter(name=name).first()

        # fields = ('name', 'regtask', 'service', 'enabled',
        #           'crontab', 'args', 'kwargs')
        # ModelForm = self.get_form(request, fields=fields)
        if request.method == "POST":
            form = PeriodicTaskPreloadForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                obj = self.save_form(request, form, change=False)
                self.save_model(request, obj, form, False)
                change_message = self.construct_change_message(request, form, None, True)
                self.log_addition(request, obj, change_message)
                obj_url = reverse(
                    "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                    args=(quote(obj.pk),),
                    current_app=self.admin_site.name,
                )
                msg_dict = {
                    "name": opts.verbose_name,
                    "obj": format_html('<a href="{}">{}</a>', quote(obj_url), obj),
                }
                msg = _('The {name} "{obj}" was added successfully.')
                self.message_user(request, format_html(msg, **msg_dict), messages.SUCCESS)
                return HttpResponseRedirect(_from)
        if obj:
            self.message_user(request, "Editing existing preload task", messages.WARNING)

        adminForm = helpers.AdminForm(
            PeriodicTaskPreloadForm(self.get_changeform_initial_data(request), instance=obj),
            [(None, {"fields": ["name", "task", "args", ("service", "crontab", "enabled"), "kwargs"]})],
            # Clear prepopulated fields on a view-only form to avoid a crash.
            {},
            [],
            model_admin=self,
        )

        context = {
            "add": True,
            "change": False,
            "has_view_permission": False,
            "has_add_permission": True,
            "has_change_permission": True,
            "has_delete_permission": False,
            "has_editable_inline_admin_formsets": False,
            "has_file_field": False,
            "has_absolute_url": True,
            "absolute_url": None,
            "form_url": "",
            "opts": opts,
            "is_popup": False,
            "adminform": adminForm,
            # 'content_type_id': get_content_type_for_model(self.model).pk,
            "save_as": False,
            "save_on_top": False,
            # 'to_field_var': TO_FIELD_VAR,
            # 'is_popup_var': IS_POPUP_VAR,
            "app_label": app_label,
        }
        return TemplateResponse(
            request,
            [
                "admin/%s/%s/change_form.html" % (app_label, opts.model_name),
                "admin/%s/change_form.html" % app_label,
                "admin/change_form.html",
            ],
            context,
        )

    def schedule(self, obj):
        fmt = "{{no schedule}}"
        if obj.interval:
            fmt = "{0.interval}"
        elif obj.crontab:
            fmt = "{0.crontab}"
        elif obj.solar:
            fmt = "{0.solar}"
        return fmt.format(obj)


class CrontabScheduleAdmin(admin.admin.ModelAdmin):
    list_display = ("minute", "hour", "day_of_month", "month_of_year")
