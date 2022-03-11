from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from admin_extra_urls.decorators import button
from admin_extra_urls.mixins import ExtraUrlMixin

from unicef_rest_framework.utils import humanize_size

from etools_datamart.libs.admin_filters import SizeFilter, StatusFilter


def queue(modeladmin, request, queryset):
    from unicef_rest_framework.tasks import preload
    for t in queryset:
        preload.apply_async(args=[t.id])


# class PreloadForm(forms.ModelForm):
#     class Meta:
#         model = Preload
#         fields = '__all__'
#         widgets = {
#             'params': JSONEditor,
#             # 'params': JSONEditorWidget({}, collapsed=False),
#         }


class PreloadAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('url', 'as_user', 'format',
                    'enabled', 'last_run',
                    'status_code', 'size', 'response_ms', 'preview')
    date_hierarchy = 'last_run'
    search_fields = ('url',)
    list_filter = (('status_code', StatusFilter), 'enabled', SizeFilter)
    actions = [queue, ]

    def format(self, obj):
        return obj.params.get('format', '')

    def preview(self, obj):
        return mark_safe("<a href='{0}' title='{0}' target='_new'>preview</a>".format(obj.get_full_url()))

    @button(label='Goto API')
    def goto(self, request, pk):
        obj = self.model.objects.get(id=pk)
        return HttpResponseRedirect(obj.get_full_url())

    def size(self, obj):
        if obj.response_length:
            return mark_safe("<nobr>{0}</nobr>".format(humanize_size(obj.response_length)))

    size.admin_order_field = 'response_length'

    @button()
    def queue(self, request, id):
        from unicef_rest_framework.tasks import preload
        preload.apply_async(args=[id])

    @button()
    def checkurl(self, request, id):
        target = self.model.objects.get(id=id)
        try:
            target.check_url(True)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)
