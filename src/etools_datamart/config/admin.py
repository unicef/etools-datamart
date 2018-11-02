from django.contrib.admin import AdminSite
from django.contrib.admin.apps import SimpleAdminConfig
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy


def reset_counters(request):
    from etools_datamart.apps.tracking.utils import reset_all_counters
    reset_all_counters()
    return HttpResponseRedirect('..')


def refresh_counters(request):
    from etools_datamart.apps.tracking.utils import refresh_all_counters
    refresh_all_counters()
    return HttpResponseRedirect('..')


class DatamartAdminSite(AdminSite):
    site_title = gettext_lazy('Datamart site admin')

    site_header = gettext_lazy('Datamart administration')

    def app_index(self, request, app_label, extra_context=None):
        if app_label == 'tracking':
            from etools_datamart.apps.tracking.utils import get_all_counters
            extra_context = {'numbers': get_all_counters()}
        return super().app_index(request, app_label, extra_context)

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        urls += [
            path('tracking/reset/', self.admin_view(reset_counters), name='tracking-reset'),
            path('tracking/refresh/', self.admin_view(refresh_counters), name='tracking-refresh')
        ]
        return urls


class AdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""
    default_site = 'etools_datamart.config.admin.DatamartAdminSite'

    def ready(self):
        super().ready()
        self.module.autodiscover()
