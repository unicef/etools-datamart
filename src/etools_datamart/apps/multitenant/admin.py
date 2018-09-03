# -*- coding: utf-8 -*-
from admin_extra_urls.extras import ExtraUrlMixin
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

from etools_datamart.state import state


class TenantChangeList(ChangeList):
    IGNORED_PARAMS = ['_schemas', ]

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


class TenantModelAdmin(ExtraUrlMixin, ModelAdmin):
    actions = None

    def get_queryset(self, request):
        return super().get_queryset(request)

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_object(self, request, object_id, from_field=None):
        pk, schema = object_id.split('-')
        queryset = self.get_queryset(request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            pk = field.to_python(pk)
            state.schemas = [schema]
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
