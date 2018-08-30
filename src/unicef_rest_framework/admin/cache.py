# -*- coding: utf-8 -*-

import logging
import re
import uuid

from admin_extra_urls.extras import action, ExtraUrlMixin, link
from django import forms
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.cache import cache
from django.db.models import F
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from unicef_rest_framework.cache import humanize_ttl, parse_ttl
from unicef_rest_framework.forms import CacheVersionForm
from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)


class CacheUpdateForm(forms.Form):
    viewset = forms.CharField()


class CacheVersionAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('name', 'cache_version', 'get_cache_ttl', 'cache_key')
    search_fields = ('name', 'viewset')
    actions = ['incr_version', 'reset_version', 'generate_cache_token']
    readonly_fields = ('cache_key', )
    list_filter = ('hidden',)
    form = CacheVersionForm

    def get_queryset(self, request):
        return super(CacheVersionAdmin, self).get_queryset(request). \
            defer('linked_models'). \
            select_related(*self.raw_id_fields)

    def has_add_permission(self, request):
        return False

    def get_cache_ttl(self, obj):
        if re.search(r'[smhdwy]', obj.cache_ttl):
            return "{} ({})".format(obj.cache_ttl, parse_ttl(obj.cache_ttl))
        else:
            return "{} ({})".format(obj.cache_ttl, humanize_ttl(obj.cache_ttl))

    get_cache_ttl.short_description = 'ttl'
    get_cache_ttl.admin_order_field = 'cache_ttl'

    @action(label='View Service')
    def goto_service(self, request, pk):
        url = reverse("admin:core_service_change", args=[pk])
        return HttpResponseRedirect(url)

    @link(label='Reset cache', css_class="btn btn-danger", icon="fa fa-warning icon-white")
    def reset_cache(self, request):
        opts = self.model._meta
        context = dict(
            self.admin_site.each_context(request),
            opts=opts,
            app_label=opts.app_label,
            message="Are you sure to clear and RESET the whole cache ?",
            description="the cache will be deleted and all versions reset to 1",
            info="""<pre>
            cache.clear()
            Service.objects.update(cache_version=1)
            </pre>
            """
        )
        if request.method == 'POST':
            cache.clear()
            Service.objects.update(cache_version=1)
            return HttpResponseRedirect(reverse(admin_urlname(opts,
                                                              'changelist')))

        return TemplateResponse(request,
                                'admin/unicef_rest_framework/confirm.html',
                                context)

    @action(label='Invalidate Cache')
    def increment(self, request, pk):
        service = Service.objects.get(id=pk)
        service.invalidate_cache()

    @action(label='Generate Cache Token')
    def generate_cache_token_single(self, request, pk):
        self.generate_cache_token(request, Service.objects.filter(id=pk))

    def incr_version(self, request, queryset):
        queryset.update(version=F("cache_version") + 1)

    incr_version.short_description = "Increment version"

    def reset_version(self, request, queryset):
        queryset.update(version=1)

    incr_version.short_description = "Increment version"

    def generate_cache_token(self, request, queryset):
        for r in queryset.all():
            r.cache_key = "{}{}".format(uuid.uuid4().hex, uuid.uuid1().hex)
            r.save()
