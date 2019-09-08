from django.contrib import admin

from admin_extra_urls.extras import action, ExtraUrlMixin

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
    list_display = ('url', 'as_user', 'enabled', 'last_run', 'status_code', 'response_length', 'response_ms')
    date_hierarchy = 'last_run'
    search_fields = ('url',)
    list_filter = (StatusFilter, 'enabled', SizeFilter)
    actions = [queue, ]
    # form = PreloadForm
    # readonly_fields = ('params',)
    # formfield_overrides = {
    #     JSONField: {'widget': JSONEditor},
    # }

    @action()
    def queue(self, request, id):
        from unicef_rest_framework.tasks import preload
        preload.apply_async(args=[id])
