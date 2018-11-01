import logging

from admin_extra_urls.extras import action, ExtraUrlMixin, link
from django import forms
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.template.response import TemplateResponse
from unicef_security.azure import Synchronizer, SyncResult
from unicef_security.models import BusinessArea, Region, Role, User
from unicef_security.sync import load_business_area, load_region

logger = logging.getLogger(__name__)


@admin.register(Region)
class RegionAdmin(ExtraUrlMixin, ModelAdmin):
    list_display = ['code', 'name']

    @link()
    def sync(self, request):
        load_region()


@admin.register(BusinessArea)
class BusinessAreaAdmin(ExtraUrlMixin, ModelAdmin):
    list_display = ['code', 'name', 'long_name', 'region']
    list_filter = ['region']
    search_fields = ('name',)

    @link()
    def sync(self, request):
        try:
            load_business_area()
        except Exception as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)


class LoadUsersForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea)


@admin.register(User)
class UserAdmin2(ExtraUrlMixin, UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_superuser']
    list_filter = ['is_superuser', 'is_staff']
    search_fields = ['username', ]

    # @link()
    # def sync(self, request):
    #     from .tasks import sync_users
    #     sync_users.delay()
    #     self.message_user(request, "User synchronization scheduled")

    @action(label='Sync')
    def sync_user(self, request, pk):
        obj = self.get_object(request, pk)
        try:
            syncronizer = Synchronizer()
            syncronizer.sync_user(obj)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)

        self.message_user(request, "User synchronized")

    @link()
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
                    result = synchronizer.fetch_users("startswith(mail,'%s')" % email)
                    total_results += result
                self.message_user(request, f"{len(total_results.created)} users have been created,"
                                           f"{len(total_results.updated)} updated."
                                           f"{len(total_results.skipped)} invalid entries found.")
        else:
            form = LoadUsersForm()
        ctx['form'] = form
        return TemplateResponse(request, 'admin/load_users.html', ctx)


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ['user', 'group']
