# -*- coding: utf-8 -*-

import logging

from admin_extra_urls.extras import ExtraUrlMixin
from django import forms
from django.contrib import admin

logger = logging.getLogger(__name__)


class CacheUpdateForm(forms.Form):
    viewset = forms.CharField()


class AuthorizationAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('service', 'user', 'group', 'policy')
    search_fields = ('user__username', )
    list_filter = ('policy', 'group')
