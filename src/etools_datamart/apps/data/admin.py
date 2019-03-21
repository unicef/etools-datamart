# -*- coding: utf-8 -*-
import logging
from time import time

from django.contrib import messages
from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponseRedirect
from django.urls import reverse

from admin_extra_urls.extras import link
from adminactions.actions import export_as_csv, export_as_xls, mass_update
from adminfilters.filters import AllValuesComboFilter
from crashlog.middleware import process_exception
from humanize import naturaldelta

from unicef_rest_framework.models import Service

from etools_datamart.apps.multitenant.admin import SchemaFilter
from etools_datamart.config import settings
from etools_datamart.libs.truncate import TruncateTableMixin

from . import models

logger = logging.getLogger(__name__)


class DatamartChangeList(ChangeList):
    pass


class DataModelAdmin(TruncateTableMixin, ModelAdmin):
    actions = [mass_update, export_as_csv, export_as_xls]

    def get_list_filter(self, request):
        if SchemaFilter not in self.list_filter:
            self.list_filter = (SchemaFilter,) + self.list_filter

        if 'last_modify_date' not in self.list_filter:
            self.list_filter = self.list_filter + ('last_modify_date',)
        return self.list_filter

    def get_changelist(self, request, **kwargs):
        return DatamartChangeList

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # def get_readonly_fields(self, request, obj=None):
    #     if not request.user.is_superuser or not settings.DEBUG:
    #         self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
    #     return self.readonly_fields
    #
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if request.method == 'POST' and not request.user.is_superuser:
    #         redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
    #                                                            self.opts.model_name))
    #
    #         self.message_user(request, "This admin is read-only. Record not saved.", level=messages.WARNING)
    #         return HttpResponseRedirect(redirect_url)
    #     return self._changeform_view(request, object_id, form_url, extra_context)

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
            res = self.model.loader.task.delay()
            if settings.CELERY_TASK_ALWAYS_EAGER:  # pragma: no cover
                stop = time()
                duration = stop - start
                self.message_user(request, "Data loaded in %s. %s" % (naturaldelta(duration),
                                                                      res.result),
                                  messages.SUCCESS)
            else:
                self.message_user(request, "ETL task scheduled", messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            process_exception(e)
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                              'changelist')))

    @link()
    def refresh(self, request):
        try:
            start = time()
            res = self.model.loader.task.apply()
            stop = time()
            duration = stop - start
            self.message_user(request, "Data loaded in %s. %s" % (naturaldelta(duration),
                                                                  res.result),
                              messages.SUCCESS)
        except Exception as e:  # pragma: no cover
            process_exception(e)
            self.message_user(request, str(e), messages.ERROR)
        finally:
            return HttpResponseRedirect(reverse(admin_urlname(self.model._meta,
                                                              'changelist')))


@register(models.PMPIndicators)
class PMPIndicatorsAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ('country_name', 'partner_name', 'partner_type', 'area_code')
    list_filter = (('partner_type', AllValuesComboFilter),
                   ('pd_ssfa_status', AllValuesComboFilter),
                   )
    search_fields = ('partner_name',)
    date_hierarchy = 'pd_ssfa_creation_date'


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


@register(models.InterventionByLocation)
class InterventionByLocationAdmin(DataModelAdmin, TruncateTableMixin):
    list_display = ('country_name', 'title', 'document_type',
                    'location_name', 'number', 'status')
    list_filter = (SchemaFilter,
                   ('document_type', AllValuesComboFilter),
                   ('status', AllValuesComboFilter),
                   'start_date',
                   )
    search_fields = ('number', 'title')
    date_hierarchy = 'start_date'


@register(models.FAMIndicator)
class FAMIndicatorAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'month',)
    list_filter = (SchemaFilter, 'month',)
    date_hierarchy = 'month'


@register(models.UserStats)
class UserStatsAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'month', 'total', 'unicef', 'logins', 'unicef_logins')
    list_filter = (SchemaFilter, 'month',)
    date_hierarchy = 'month'


@register(models.HACT)
class HACTAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'year',
                    'microassessments_total',
                    'programmaticvisits_total',
                    'followup_spotcheck', 'completed_spotcheck',
                    'completed_hact_audits', 'completed_special_audits')
    list_filter = (SchemaFilter, 'year', 'last_modify_date')


@register(models.GatewayType)
class GatewayTypeAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'name', 'admin_level', 'source_id')


@register(models.Location)
class LocationAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'name', 'latitude', 'longitude')
    readonly_fields = ('parent', 'gateway')


@register(models.FundsReservation)
class FundsReservationAdmin(DataModelAdmin):
    list_display = ('country_name', 'schema_name', 'fr_number', 'fr_type', 'wbs')
    date_hierarchy = 'start_date'


@register(models.PDIndicator)
class PDIndicatorAdmin(DataModelAdmin):
    list_display = ('title', 'unit', 'display_type')
    # list_filter = ('disaggregatable', )


@register(models.Travel)
class TravelAdmin(DataModelAdmin):
    list_display = ('traveler_email', 'supervisor_email', 'created')
    date_hierarchy = 'created'
    list_filter = ('international_travel', 'office_name', 'status',
                   'completed_at', 'approved_at', 'end_date', 'start_date')
    search_fields = ('office_name', 'traveler_email',)


@register(models.Partner)
class PartnerAdmin(DataModelAdmin):
    list_display = ('name', 'partner_type', 'vendor_number', 'cso_type', 'rating')
    date_hierarchy = 'created'
    list_filter = ('partner_type', 'hidden', 'cso_type', 'rating')
    search_fields = ('vendor_number', 'name',)


@register(models.TravelActivity)
class TravelActivityAdmin(DataModelAdmin):
    list_display = ('travel_reference_number',
                    'date',
                    'location_name',
                    'partner_name',
                    'primary_traveler')
