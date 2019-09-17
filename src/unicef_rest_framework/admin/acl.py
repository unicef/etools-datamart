# -*- coding: utf-8 -*-

import logging

from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, widgets
from django.contrib.admin.helpers import AdminForm
from django.contrib.auth.models import Group
from django.contrib.postgres.forms import SimpleArrayField
from django.template.response import TemplateResponse

from admin_extra_urls.extras import ExtraUrlMixin, link
from adminactions.mass_update import mass_update, MassUpdateForm

from unicef_rest_framework.models import Service, UserAccessControl
from unicef_rest_framework.models.acl import AbstractAccessControl, GroupAccessControl

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
    list_display = ('user', 'service', 'rate', 'serializers', 'policy')
    list_filter = ('user', 'policy', 'service')
    search_fields = ('user', 'service',)
    form = UserACLAdminForm

    def get_queryset(self, request):
        return super(UserAccessControlAdmin, self).get_queryset(request).select_related(*self.raw_id_fields)


class GroupAccessControlForm(forms.Form):
    overwrite_existing = forms.BooleanField(help_text="Overwrite existing entries", required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    policy = forms.ChoiceField(choices=AbstractAccessControl.POLICIES)
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(),
                                              widget=widgets.FilteredSelectMultiple('Services', False)
                                              )
    rate = forms.CharField(max_length=100)
    serializers = SimpleArrayField(forms.CharField(),
                                   max_length=255)


class LazyMassUpdateForm(MassUpdateForm):
    _no_sample_for = ['last_modify_user', ]


class SectionFilter(SimpleListFilter):
    title = 'Section'  # or use _('country') for translated title
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        return [('.datamart.', 'Datamart'),
                ('.etools.', 'eTools'),
                ('.prp.', 'PRP')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(service__name__contains=self.value())
        return queryset


class GroupAccessControlAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('group', 'service', 'rate', 'serializers', 'policy')
    list_filter = ('group', 'policy', SectionFilter)
    search_fields = ('group__name', 'service__name',)
    form = GroupACLAdminForm
    autocomplete_fields = ('group',)
    actions = [mass_update]
    mass_update_form = LazyMassUpdateForm

    # filter_horizontal = ('services',)

    def get_queryset(self, request):
        return super(GroupAccessControlAdmin, self).get_queryset(request).select_related(*self.raw_id_fields)

    def has_add_permission(self, request):
        return False

    @link()
    def add_acl(self, request):
        opts = self.model._meta
        ctx = {
            'opts': opts,
            'add': False,
            'has_view_permission': True,
            'has_editable_inline_admin_formsets': True,
            'app_label': opts.app_label,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'media': self.media,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': True,
        }
        if request.method == 'POST':
            form = GroupAccessControlForm(request.POST)
            if form.is_valid():
                services = form.cleaned_data.pop('services')
                group = form.cleaned_data.pop('group')
                overwrite_existing = form.cleaned_data.pop('overwrite_existing')

                for service in services:
                    if overwrite_existing:
                        GroupAccessControl.objects.update_or_create(service=service,
                                                                    group=group,
                                                                    defaults=form.cleaned_data)
                    else:
                        GroupAccessControl.objects.update_or_create(service=service,
                                                                    group=group,
                                                                    defaults=form.cleaned_data)
                self.message_user(request, 'ACLs created')

        else:
            form = GroupAccessControlForm(initial={'rate': '*',
                                                   'policy': AbstractAccessControl.POLICY_ALLOW,
                                                   'serializers': 'std'})
        ctx['adminform'] = AdminForm(form,
                                     [(None, {'fields': ['overwrite_existing',
                                                         ['group', 'policy'],
                                                         'services',
                                                         ['rate', 'serializers']]})],
                                     {})
        ctx['media'] = self.media + form.media
        return TemplateResponse(request, 'admin/unicef_rest_framework/groupaccesscontrol/add.html', ctx)
