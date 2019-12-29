from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from admin_extra_urls.extras import action, ExtraUrlMixin

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
    list_display = ('name', 'as_user', 'format',
                    'enabled', 'refresh', 'last_run',
                    'status_code', 'size', 'response_ms', 'api', 'download')
    date_hierarchy = 'last_run'
    search_fields = ('url',)
    list_filter = (StatusFilter, 'enabled', SizeFilter, 'refresh')
    actions = [queue, check]

    def format(self, obj):
        return obj.stem

    def api(self, obj):
        return mark_safe("<a href='{0}' title='{0}' target='_new'>preview</a>".format(obj.get_full_url()))

    def download(self, obj):
        if obj.etag:
            url = reverse('urf:export-fetch', args=[obj.pk])
            return mark_safe("<a href='{0}' title='{0}' target='_new'>download</a>".format(url))
        return '--'

    def size(self, obj):
        if obj.response_length:
            return mark_safe("<nobr>{0}</nobr>".format(humanize_size(obj.response_length)))

    size.admin_order_field = 'response_length'

    @action()
    def check_file(self, request, pk):
        obj = self.model.objects.get(id=pk)
        if obj.check_file():
            self.message_user(request, 'File exists.')
        else:
            self.message_user(request, 'File does not exists.', messages.ERROR)

    @action(label='Goto API')
    def goto(self, request, pk):
        obj = self.model.objects.get(id=pk)
        return HttpResponseRedirect(obj.get_full_url())

    @action()
    def queue(self, request, pk):
        from unicef_rest_framework.tasks import export
        export.apply_async(args=[pk])

    @action()
    def run(self, request, pk):
        from unicef_rest_framework.tasks import export
        export(pk)

    @action(label='download')
    def _download(self, request, pk):
        obj = self.model.objects.get(id=pk)
        url = reverse('urf:export-fetch', args=[obj.pk])
        return HttpResponseRedirect(url)
