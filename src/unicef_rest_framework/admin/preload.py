from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.postgres.fields import JSONField

from admin_extra_urls.extras import action, ExtraUrlMixin
from jsoneditor.forms import JSONEditor

from unicef_rest_framework.models import Preload


class StatusFilter(SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return zip(['2xx', '3xx', '4xx', '5xx'],
                   ['2xx', '3xx', '4xx', '5xx'])

    def value(self):
        return self.used_parameters.get(self.parameter_name)

    def queryset(self, request, queryset):
        if self.value():
            flt = int(self.value()[0]) * 100
            return queryset.filter(last_status_code__gte=flt,
                                   last_status_code__lt=(flt + 100),
                                   )
        return queryset


def queue(modeladmin, request, queryset):
    from unicef_rest_framework.tasks import preload
    for t in queryset:
        preload.apply_async(args=[t.id])


class PreloadForm(forms.ModelForm):
    class Meta:
        model = Preload
        fields = '__all__'
        widgets = {
            'params': JSONEditor,
            # 'params': JSONEditorWidget({}, collapsed=False),
        }


class PreloadAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('url', 'as_user', 'enabled', 'last_run', 'last_status_code')
    date_hierarchy = 'last_run'
    search_fields = ('url',)
    list_filter = (StatusFilter, 'enabled')
    actions = [queue, ]
    form = PreloadForm
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }

    @action()
    def queue(self, request, id):
        from unicef_rest_framework.tasks import preload
        preload.apply_async(args=[id])
