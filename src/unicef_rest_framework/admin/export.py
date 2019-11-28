from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from admin_extra_urls.extras import action, ExtraUrlMixin

from unicef_rest_framework.utils import humanize_size

from etools_datamart.libs.admin_filters import SizeFilter, StatusFilter


def queue(modeladmin, request, queryset):
    from unicef_rest_framework.tasks import preload
    for t in queryset:
        preload.apply_async(args=[t.id])


class ExportAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('url', 'as_user', 'format',
                    'enabled', 'refresh', 'last_run',
                    'status_code', 'size', 'response_ms', 'api')
    date_hierarchy = 'last_run'
    search_fields = ('url',)
    list_filter = (StatusFilter, 'enabled', SizeFilter, 'refresh')
    actions = [queue, ]

    def format(self, obj):
        return obj.params.get('format', '')

    def api(self, obj):
        return mark_safe("<a href='{0}' title='{0}' target='_new'>preview</a>".format(obj.get_full_url()))

    @action(label='Goto API')
    def goto(self, request, pk):
        obj = self.model.objects.get(id=pk)
        return HttpResponseRedirect(obj.get_full_url())

    def size(self, obj):
        if obj.response_length:
            return mark_safe("<nobr>{0}</nobr>".format(humanize_size(obj.response_length)))

    size.admin_order_field = 'response_length'

    @action()
    def queue(self, request, id):
        from unicef_rest_framework.tasks import export
        export.apply_async(args=[id])

    @action()
    def run(self, request, id):
        from unicef_rest_framework.tasks import export
        export(id)

    @action()
    def check_url(self, request, id):
        target = self.model.objects.get(id=id)
        try:
            target.check_url(True)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)
