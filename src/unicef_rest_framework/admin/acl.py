# -*- coding: utf-8 -*-

import logging

from django import forms
from django.contrib import admin
from unicef_rest_framework.models import UserAccessControl
from unicef_rest_framework.models.acl import GroupAccessControl

logger = logging.getLogger(__name__)


class UserACLAdminForm(forms.ModelForm):
    class Meta:
        model = UserAccessControl
        fields = ('user', 'service', 'serializers', 'policy', 'rate')


class GroupACLAdminForm(forms.ModelForm):
    class Meta:
        model = GroupAccessControl
        fields = ('group', 'service', 'serializers', 'policy', 'rate')


class UserAccessControlAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'rate', 'serializers')
    list_filter = ('user', 'service',)
    search_fields = ('user', 'service',)
    form = UserACLAdminForm

    def get_queryset(self, request):
        return super(UserAccessControlAdmin, self).get_queryset(request).select_related(*self.raw_id_fields)


class GroupAccessControlAdmin(admin.ModelAdmin):
    list_display = ('group', 'service', 'rate', 'serializers')
    list_filter = ('group', 'service',)
    search_fields = ('group', 'service',)
    form = GroupACLAdminForm

    def get_queryset(self, request):
        return super(GroupAccessControlAdmin, self).get_queryset(request).select_related(*self.raw_id_fields)
