# -*- coding: utf-8 -*-

import logging

import requests
from admin_extra_urls.extras import action, ExtraUrlMixin
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models.filter import SystemFilter, SystemFilterFieldRule

logger = logging.getLogger(__name__)


class SystemFilterRuleInline(TabularInline):
    model = SystemFilterFieldRule
    list_display = ('field', 'value', 'override_field')


# class SystemFilterParamInline(TabularInline):
#     model = SystemFilterParam
#     list_display = ('param', 'value')


class SystemFilterAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('service', 'user', 'group', 'handler')
    readonly_fields = ('handler',)
    list_filter = ('service', 'user')
    search_fields = ('service__name',)
    inlines = [SystemFilterRuleInline]

    @action()
    def test(self, request, pk):
        if not pk:
            return
        rule = SystemFilter.objects.get(pk=pk)
        try:
            rule.service.view().get_queryset().filter(**rule.get_filters())
            self.message_user(request, "Filter seems ok")
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)

        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_change' % info,
                                            args=[pk]))

    @action()
    def view(self, request, pk):
        if not pk:
            return
        rule = SystemFilter.objects.get(pk=pk)
        try:
            filter = rule.get_querystring()
            url = "{}{}?{}".format(settings.DATAMART_SERVER,
                                   rule.service.endpoint,
                                   filter)
            res = requests.get(url)
            if res.status_code == 200:
                return HttpResponseRedirect(url)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)

        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_change' % info,
                                            args=[pk]))
