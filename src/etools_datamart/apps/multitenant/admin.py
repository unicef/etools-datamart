from django.contrib import messages
from django.contrib.admin import ListFilter, ModelAdmin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.db import connections
from django.http import HttpResponseRedirect
from django.urls import reverse

from admin_extra_urls.mixins import ExtraUrlMixin

from etools_datamart.apps.core.admin_mixins import DisplayAllMixin, ReadOnlyMixin


class TenantChangeList(ChangeList):
    IGNORED_PARAMS = ['country_name', ]

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse('admin:%s_%s_change' % (self.opts.app_label,
                                               self.opts.model_name),
                       args=[quote(f"{pk}-{ result.schema}")],
                       current_app=self.model_admin.admin_site.name)

    def get_filters_params(self, params=None):
        ret = super().get_filters_params(params)
        for ignored in self.IGNORED_PARAMS:
            if ignored in ret:
                del ret[ignored]
        return ret


class SchemaFilter(ListFilter):
    template = 'schemafilter.html'
    title = 'country_name'
    parameter_name = 'country_name'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.request = request
        self.model = model
        self.model_admin = model_admin
        self.conn = connections['etools']
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def choices(self, changelist):
        self.all_filters = changelist.get_query_string({"from": self.request.path}, [])
        value = self.request.GET.get(self.parameter_name, "").split(",")
        yield {
            'selected': value == [''],
            'query_string': changelist.get_query_string({}, [self.parameter_name]),
            'display': 'All',
        }
        for lookup in self.conn.get_tenants():
            yield {
                'selected': str(lookup.schema_name) in value,
                'query_string': changelist.get_query_string({self.parameter_name: lookup.schema_name}, []),
                'display': lookup.name,
            }

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name, "")
        if value:
            queryset = queryset.filter_schemas(*value.split(","))
        else:
            queryset = queryset.filter_schemas(None)
        return queryset


class EToolsModelAdmin(ExtraUrlMixin, DisplayAllMixin, ReadOnlyMixin, ModelAdmin):

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))

            self.message_user(request, "This admin is read-only. Record not saved.", level=messages.WARNING)
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)


class TenantModelAdmin(ExtraUrlMixin, DisplayAllMixin, ReadOnlyMixin, ModelAdmin):
    list_filter = [SchemaFilter, ]

    # def get_queryset(self, request):
    #     super().get_queryset(request)

    def get_object(self, request, object_id, from_field=None):
        pk, schema = object_id.split('-')
        queryset = self.get_queryset(request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            pk = field.to_python(pk)
            conn = connections['etools']
            conn.set_schemas([schema])
            return queryset.get(**{field.name: pk})
        except MultipleObjectsReturned:  # pragma: no cover
            raise
        except (model.DoesNotExist, ValidationError, ValueError):  # pragma: no cover
            return None

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))

            self.message_user(request, "This admin is read-only. Record not saved.", level=messages.WARNING)
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)

    def get_changelist(self, request, **kwargs):
        return TenantChangeList
