# -*- coding: utf-8 -*-
import logging
from time import time

from admin_extra_urls.extras import ExtraUrlMixin, link
from adminfilters.filters import AllValuesComboFilter
from django.contrib import messages
from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponseRedirect
from django.urls import reverse
from humanize import naturaldelta
from unicef_rest_framework.models import Service

from etools_datamart.apps.etl.tasks import load_fam_indicator, load_intervention, load_pmp_indicator, load_user_report
from etools_datamart.apps.multitenant.admin import SchemaFilter
from etools_datamart.config import settings
from etools_datamart.libs.truncate import TruncateTableMixin

from . import models

logger = logging.getLogger(__name__)


class DatamartChangeList(ChangeList):
    pass


class DataModelAdmin(ExtraUrlMixin, ModelAdmin):
    actions = None
    load_handler = None
    list_filter = (SchemaFilter,)

    def get_changelist(self, request, **kwargs):
        return DatamartChangeList

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
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
    def invalidate_cache(self, request):
        for s in Service.objects.all():
            if s.managed_model == self.model:
                s.invalidate_cache()

    @link()
    def api(self, request):
        for s in Service.objects.all():
            if s.managed_model == self.model:
                return HttpResponseRedirect(s.endpoint)
        return ""  # pragma: no cover

    @link()
    def queue(self, request):
        try:
            start = time()
            self.model._etl_task.delay()
            if settings.CELERY_TASK_ALWAYS_EAGER:  # pragma: no cover
                stop = time()
                duration = stop - start
                self.message_user(request, "Data loaded in %s" % naturaldelta(duration), messages.SUCCESS)
            else:
                self.message_user(request, "ETL task scheduled", messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                              'changelist')))

    # @link()
    # def refresh(self, request):
    #     try:
    #         start = time()
    #         self.model._etl_task.apply()
    #         stop = time()
    #         duration = stop - start
    #         self.message_user(request, "Data loaded in %s" % naturaldelta(duration), messages.SUCCESS)
    #     except Exception as e:  # pragma: no cover
    #         process_exception(e)
    #         self.message_user(request, str(e), messages.ERROR)
    #     finally:
    #         return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
    #                                                           'changelist')))


@register(models.PMPIndicators)
class PMPIndicatorsAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ('country_name', 'partner_name', 'partner_type', 'business_area_code')
    list_filter = (SchemaFilter,
                   ('partner_type', AllValuesComboFilter),
                   )
    search_fields = ('partner_name',)
    date_hierarchy = 'pd_ssfa_creation_date'
    load_handler = load_pmp_indicator


@register(models.Intervention)
class InterventionAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ('country_name', 'title', 'document_type', 'number', 'status')
    list_filter = (SchemaFilter,
                   ('document_type', AllValuesComboFilter),
                   ('status', AllValuesComboFilter),
                   'start_date',
                   )
    search_fields = ('number', 'title')
    date_hierarchy = 'start_date'
    load_handler = load_intervention


@register(models.FAMIndicator)
class FAMIndicatorAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'month',)
    list_filter = (SchemaFilter, 'month',)
    load_handler = load_fam_indicator
    date_hierarchy = 'month'


@register(models.UserStats)
class UserStatsAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'month', 'total', 'unicef', 'logins', 'unicef_logins')
    list_filter = (SchemaFilter, 'month')
    load_handler = load_user_report
    date_hierarchy = 'month'
