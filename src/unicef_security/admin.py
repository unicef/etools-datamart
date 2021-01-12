import logging

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, widgets
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.forms import Form
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from admin_extra_urls.decorators import action
from admin_extra_urls.mixins import ExtraUrlMixin

from unicef_security.graph import default_group, Synchronizer, SyncResult
from unicef_security.models import BusinessArea, Region, User
from unicef_security.sync import load_business_area, load_region

logger = logging.getLogger(__name__)


def admin_reverse(model, page="changelist"):
    return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_{page}")


@admin.register(Region)
class RegionAdmin(ExtraUrlMixin, ModelAdmin):
    list_display = ['code', 'name']

    @action()
    def sync(self, request):
        load_region()


@admin.register(BusinessArea)
class BusinessAreaAdmin(ExtraUrlMixin, ModelAdmin):
    list_display = ['code', 'name', 'long_name', 'region', 'country']
    list_filter = ['region', 'country']
    search_fields = ('name',)

    @action()
    def sync(self, request):
        try:
            load_business_area()
        except Exception as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)


class LoadUsersForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea)


class FF(Form):
    selection = forms.CharField()


@admin.register(User)
class UserAdmin2(ExtraUrlMixin, UserAdmin):
    list_display = ['username', 'display_name', 'email', 'is_staff',
                    'is_active', 'is_superuser', 'is_linked', 'last_login']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    search_fields = ['username', 'display_name', 'email']
    fieldsets = (
        (None, {'fields': (('username', 'azure_id'), 'password')}),
        (_('Personal info'), {'fields': (('first_name', 'last_name',),
                                         ('email', 'display_name'),
                                         ('job_title',),
                                         )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('azure_id', 'job_title', 'display_name')

    def is_linked(self, obj):
        return bool(obj.azure_id)

    is_linked.boolean = True

    @action()
    def impersonate(self, request, pk):
        url = reverse('impersonate-start', args=[pk])
        return HttpResponseRedirect(url)

    @action(label='Sync')
    def sync_user(self, request, pk):
        obj = self.get_object(request, pk)
        try:
            syncronizer = Synchronizer()
            syncronizer.sync_user(obj)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)

        self.message_user(request, "User synchronized")

    @action(label='Link user')
    def link_user_data(self, request, pk):
        opts = self.model._meta
        ctx = {
            'opts': opts,
            'app_label': 'security',
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': True,
        }
        obj = self.get_object(request, pk)
        syncronizer = Synchronizer()
        try:
            if request.method == 'POST':
                if request.POST.get('selection'):
                    data = syncronizer.get_user(request.POST.get('selection'))
                    syncronizer.sync_user(obj, data['id'])
                    self.message_user(request, "User linked")
                    return None
                else:
                    ctx['message'] = 'Select one entry to link'

            data = syncronizer.search_users(obj)
            ctx['data'] = data
            return TemplateResponse(request, 'admin/link_user.html', ctx)

        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)

    @action()
    def load(self, request):
        opts = self.model._meta
        ctx = {
            'opts': opts,
            'app_label': 'security',
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': True,
        }
        if request.method == 'POST':
            form = LoadUsersForm(request.POST)
            if form.is_valid():
                synchronizer = Synchronizer()
                emails = form.cleaned_data['emails'].split()
                total_results = SyncResult()
                for email in emails:
                    result = synchronizer.fetch_users("startswith(mail,'%s')" % email,
                                                      callback=default_group)
                    total_results += result
                self.message_user(request,
                                  f"{len(total_results.created)} users have been created,"
                                  f"{len(total_results.updated)} updated."
                                  f"{len(total_results.skipped)} invalid entries found.")
        else:
            form = LoadUsersForm()
        ctx['form'] = form
        return TemplateResponse(request, 'admin/load_users.html', ctx)


class RoleForm(forms.Form):
    # overwrite_existing = forms.BooleanField(help_text="Overwrite existing entries", required=False)
    business_areas = forms.ModelMultipleChoiceField(queryset=BusinessArea.objects.all(),
                                                    widget=widgets.FilteredSelectMultiple('Services', False)
                                                    )
    user = forms.ModelChoiceField(queryset=User.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())

# @admin.register(Role)
# class RoleAdmin(ExtraUrlMixin, ModelAdmin):
#     list_display = ['user', 'group', 'business_area']
#     search_fields = ('user',)
#     list_filter = ('group', ('business_area', RelatedFieldComboFilter))
#
#     def has_add_permission(self, request):
#         return False
#
#     @action()
#     def add_grants(self, request):
#         opts = self.model._meta
#         ctx = {
#             'opts': opts,
#             'add': False,
#             'has_view_permission': True,
#             'has_editable_inline_admin_formsets': True,
#             'app_label': opts.app_label,
#             'change': True,
#             'is_popup': False,
#             'save_as': False,
#             'media': self.media,
#             'has_delete_permission': False,
#             'has_add_permission': False,
#             'has_change_permission': True,
#         }
#         if request.method == 'POST':
#             form = RoleForm(request.POST)
#             if form.is_valid():
#                 user = form.cleaned_data.pop('user')
#                 business_areas = form.cleaned_data.pop('business_areas')
#                 group = form.cleaned_data.pop('group')
#                 # overwrite_existing = form.cleaned_data.pop('overwrite_existing')
#
#                 for business_area in business_areas:
#                     Role.objects.update_or_create(user=user,
#                                                   business_area=business_area,
#                                                   group=group)
#                 self.message_user(request, 'ACLs created')
#                 return HttpResponseRedirect(admin_reverse(Role))
#         else:
#             form = RoleForm(initial={})
#         ctx['adminform'] = AdminForm(form,
#                                      [(None, {'fields': ['user',
#                                                          'group',
#                                                          'business_areas']})],
#                                      {})
#         ctx['media'] = self.media + form.media
#         return TemplateResponse(request, 'admin/unicef_security/add_grants.html', ctx)
