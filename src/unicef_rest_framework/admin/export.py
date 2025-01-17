from datetime import datetime, timedelta

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, register
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin
from adminfilters.mixin import AdminFiltersMixin
from adminfilters.value import ValueFilter
from humanize import precisedelta

from unicef_rest_framework.models.export import ExportAccessLog
from unicef_rest_framework.utils import humanize_size

from etools_datamart.libs.admin_filters import SizeFilter, StatusFilter


def check(modeladmin, request, queryset):
    for t in queryset:
        if not t.check_file():
            t.status_code = 999
            t.response_length = 0
            t.response_ms = 0
            t.etag = ""
            t.save()


def queue(modeladmin, request, queryset):
    from unicef_rest_framework.tasks import preload

    for t in queryset:
        preload.apply_async(args=[t.id])


class ExportAdmin(AdminFiltersMixin, ExtraButtonsMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "filename",
        "as_user",
        "format",
        "enabled",
        "refresh",
        "last_run",
        "status_code",
        "size",
        "response_ms",
        "delta",
        "api",
        "download",
        "queue_task",
    )
    date_hierarchy = "last_run"
    search_fields = ("id", "url", "name", "filename", "url")
    list_filter = (
        ("as_user__username", ValueFilter.factory(title="User", lookup_name="icontains")),
        ("status_code", StatusFilter),
        SizeFilter,
        "enabled",
        "refresh",
        "format",
    )
    actions = [queue, check]
    raw_id_fields = ("as_user",)

    def format(self, obj):
        return obj.stem

    def api(self, obj):
        return mark_safe("<a href='{0}' title='{0}' target='_new'>preview</a>".format(obj.get_full_url()))

    def download(self, obj):
        if obj.etag:
            url = reverse("urf:export-fetch", args=[obj.pk])
            return mark_safe("<a href='{0}' title='{0}' target='_new'>download</a>".format(url))
        return "--"

    def queue_task(self, obj):
        opts = self.model._meta
        url = reverse("admin:%s_%s_queue" % (opts.app_label, opts.model_name), args=[obj.id])
        return mark_safe(f'<a href="{url}">queue</a>')

    def size(self, obj):
        if obj.response_length:
            return mark_safe("<nobr>{0}</nobr>".format(humanize_size(obj.response_length)))

    size.admin_order_field = "response_length"

    def delta(self, obj):
        return precisedelta(timedelta(milliseconds=obj.response_ms)) if obj else "-"

    delta.admin_order_field = "response_ms"

    @button()
    def check_file(self, request, pk):
        obj = self.model.objects.get(id=pk)
        if obj.check_file():
            self.message_user(request, "File exists.")
        else:
            self.message_user(request, "File does not exists.", messages.ERROR)

    @button(label="Goto API")
    def goto(self, request, pk):
        obj = self.model.objects.get(id=pk)
        return HttpResponseRedirect(obj.get_full_url())

    @button()
    def queue(self, request, pk):
        from unicef_rest_framework.tasks import export

        obj = self.get_object(request, pk)
        export.apply_async(args=[pk])
        self.message_user(request, f"Export generation '{obj.name}' queued", messages.SUCCESS)
        return HttpResponseRedirect(reverse("admin:unicef_rest_framework_export_changelist"))

    @button()
    def run(self, request, pk):
        from unicef_rest_framework.tasks import export

        export(pk)

    @button()
    def force_run(self, request, pk):
        from unicef_rest_framework.tasks import export

        obj = self.model.objects.get(id=pk)
        obj.status_code = -1
        obj.etag = None
        obj.save()
        export(pk)

    @button(label="Download")
    def _download(self, request, pk):
        obj = self.model.objects.get(id=pk)
        url = reverse("urf:export-fetch", args=[obj.pk])
        return HttpResponseRedirect(url)


@register(ExportAccessLog)
class ExportAccessLogAdmin(admin.ModelAdmin):
    readonly_fields = ("export", "access_history")  #

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_access_history(self, obj):
        access_history = obj.access_history
        formatted_history = []
        for entry in access_history:
            user = entry.get("u")
            timestamp_utc = entry.get("t")
            if timestamp_utc:
                try:
                    # Parse the ISO 8601 string to a datetime object
                    timestamp_utc = datetime.fromisoformat(timestamp_utc)
                    timestamp_local = timezone.localtime(timezone.make_aware(timestamp_utc))
                    formatted_timestamp = timestamp_local.strftime("%Y-%m-%d %H:%M:%S")
                    formatted_history.append(f"{user}: {formatted_timestamp}")
                except ValueError:
                    # Handle cases where the timestamp format is incorrect
                    formatted_history.append(f"{user}: Invalid timestamp")

        return ", ".join(formatted_history)

    display_access_history.short_description = "Export Access History"
    list_display = ("export", "display_access_history")
    list_filter = ("export",)
    search_fields = ("export",)
