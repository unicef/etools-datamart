# -*- coding: utf-8 -*-

import logging

from django import forms
from django.contrib import admin
from unicef_rest_framework.models import UserAccessControl

logger = logging.getLogger(__name__)


class AccessControlAdmin(admin.ModelAdmin):
    list_display = ('service', 'rate', 'serializers')
    list_filter = ('service',)
    search_fields = ('service',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AccessControlAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'serializer':
            field.widget.attrs['style'] = 'width:100%'
        elif db_field.name == 'rate':
            field.widget.attrs['style'] = 'width:80px'
        return field


class ApplicationACLAdmin(AccessControlAdmin):
    list_display = ('application',) + AccessControlAdmin.list_display
    list_filter = ('application',) + AccessControlAdmin.list_filter
    search_fields = ('application',) + AccessControlAdmin.search_fields
    raw_id_fields = select2_fields = ('application', 'service',)

    def get_queryset(self, request):
        return super(ApplicationACLAdmin, self).get_queryset(request).select_related(*self.raw_id_fields)


class UserACLAdminForm(forms.ModelForm):
    class Meta:
        model = UserAccessControl
        exclude = ()


class UserACLAdmin(AccessControlAdmin):
    list_display = ('user',) + AccessControlAdmin.list_display
    list_filter = ('user',) + AccessControlAdmin.list_filter
    search_fields = ('user',) + AccessControlAdmin.search_fields
    form = UserACLAdminForm
    raw_id_fields = select2_fields = ('user', 'service',)

    def get_queryset(self, request):
        return super(UserACLAdmin, self).get_queryset(request).select_related(*self.raw_id_fields)


class GroupACLAdmin(AccessControlAdmin):
    list_display = ('group',) + AccessControlAdmin.list_display
    list_filter = ('group',) + AccessControlAdmin.list_filter
    search_fields = ('group',) + AccessControlAdmin.search_fields
    select2_fields = ('group', 'service',)
