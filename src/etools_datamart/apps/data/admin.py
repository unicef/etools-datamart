# -*- coding: utf-8 -*-
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.urls import reverse
from time import time

from admin_extra_urls.extras import ExtraUrlMixin, link
from admin_extra_urls.mixins import _confirm_action
from django.contrib import messages
from django.contrib.admin import ModelAdmin, register, ListFilter, FieldListFilter

from adminfilters.filters import RelatedFieldComboFilter, AllValuesComboFilter, AllValuesRadioFilter, StartWithFilter
from etools_datamart.apps.etl.tasks import load_pmp_indicator
from . import models


class DataModelAdmin(ExtraUrlMixin, ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))

            self.message_user(request, "This admin is read-only. Record not saved.", level=messages.WARNING)
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)


    @link()
    def refresh(self, request):
        raise NotImplementedError

    @link()
    def truncate(self, request):
        def _action(request):
            from django.db import connection

            cursor = connection.cursor()
            cursor.execute('TRUNCATE TABLE {0}'.format(self.model._meta.db_table))

        return _confirm_action(self, request, _action, "Continuing will erase the entire content of the table.",
                               "Successfully executed", )


@register(models.PMPIndicators)
class PMPIndicatorsAdmin(DataModelAdmin):
    list_display = ('country_name', 'partner_name', 'partner_type')
    list_filter = (('country_name', AllValuesComboFilter),
                   ('partner_type', AllValuesRadioFilter),
                   )
    search_fields = ('partner_name',)
    date_hierarchy = 'pd_ssfa_creation_date'

    @link()
    def refresh(self, request):
        try:
            start = time()
            load_pmp_indicator()
            stop = time()
            duration = stop - start
            self.message_user(request, "Data loaded in %.3f" % duration)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)

        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                              'changelist')))
