from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from admin_extra_urls.decorators import button
from admin_extra_urls.mixins import ExtraUrlMixin
from adminfilters.filters import TextFieldFilter

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


class ExportAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('name', 'filename', 'as_user', 'format',
                    'enabled', 'refresh', 'last_run',
                    'status_code', 'size', 'response_ms', 'api', 'download', 'queue_task')
    date_hierarchy = 'last_run'
    search_fields = ('url', 'name', 'filename')
    list_filter = (
        TextFieldFilter.factory('as_user__username__icontains', "User"),
        ('status_code', StatusFilter),
        SizeFilter, 'enabled', 'refresh', 'format',
    )
    actions = [queue, check]
    raw_id_fields = ('as_user', )

    def format(self, obj):
        return obj.stem

    def api(self, obj):
        return mark_safe("<a href='{0}' title='{0}' target='_new'>preview</a>".format(obj.get_full_url()))

    def download(self, obj):
        if obj.etag:
            url = reverse('urf:export-fetch', args=[obj.pk])
            return mark_safe("<a href='{0}' title='{0}' target='_new'>download</a>".format(url))
        return '--'

    def queue_task(self, obj):
        opts = self.model._meta
        url = reverse('admin:%s_%s_queue' % (opts.app_label, opts.model_name), args=[obj.id])
        return mark_safe(f'<a href="{url}">queue</a>')

    def size(self, obj):
        if obj.response_length:
            return mark_safe("<nobr>{0}</nobr>".format(humanize_size(obj.response_length)))

    size.admin_order_field = 'response_length'

    @button()
    def check_file(self, request, pk):
        obj = self.model.objects.get(id=pk)
        if obj.check_file():
            self.message_user(request, 'File exists.')
        else:
            self.message_user(request, 'File does not exists.', messages.ERROR)

    @button(label='Goto API')
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

    @button(label='download')
    def _download(self, request, pk):
        obj = self.model.objects.get(id=pk)
        url = reverse('urf:export-fetch', args=[obj.pk])
        return HttpResponseRedirect(url)
