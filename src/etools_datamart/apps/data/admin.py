# -*- coding: utf-8 -*-
import logging
from time import time

from admin_extra_urls.extras import ExtraUrlMixin, link
from admin_extra_urls.mixins import _confirm_action
from adminfilters.filters import AllValuesComboFilter
from django.contrib import messages
from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponseRedirect
from django.urls import reverse
from humanize import naturaldelta

from etools_datamart.apps.etl.tasks import load_intervention, load_pmp_indicator

from . import models

logger = logging.getLogger(__name__)


class DatamartChangeList(ChangeList):
    IGNORED_PARAMS = ['_schemas', ]

    def get_filters_params(self, params=None):
        ret = super().get_filters_params(params)
        for ignored in self.IGNORED_PARAMS:
            if ignored in ret:
                del ret[ignored]
        return ret


class DataModelAdmin(ExtraUrlMixin, ModelAdmin):
    actions = None
    load_handler = None
    list_filter = (('country_name', AllValuesComboFilter),)

    def get_changelist(self, request, **kwargs):
        return DatamartChangeList

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
    def queue(self, request):
        try:
            self.model._etl_task.delay()
            self.message_user(request, "ETL task scheduled")
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                              'changelist')))

    @link()
    def refresh(self, request):
        try:
            start = time()
            # _etl_loader is set by DatamartCelery.etl()
            # used to decorate any ETL task
            self.model._etl_task.apply()
            stop = time()
            duration = stop - start
            self.message_user(request, "Data loaded in %f" % naturaldelta(duration))
        except Exception as e:
            logger.exception(e)
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                              'changelist')))

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
    list_display = ('country_name', 'partner_name', 'partner_type', 'business_area_code')
    list_filter = (('country_name', AllValuesComboFilter),
                   ('partner_type', AllValuesComboFilter),
                   )
    search_fields = ('partner_name',)
    date_hierarchy = 'pd_ssfa_creation_date'
    load_handler = load_pmp_indicator


@register(models.Intervention)
class InterventionAdmin(DataModelAdmin):
    list_display = ('country_name', 'title', 'document_type', 'number', 'status')
    list_filter = (('country_name', AllValuesComboFilter),
                   ('document_type', AllValuesComboFilter),
                   ('status', AllValuesComboFilter),
                   'start_date',
                   )
    search_fields = ('number', 'title')
    date_hierarchy = 'start_date'
    load_handler = load_intervention
