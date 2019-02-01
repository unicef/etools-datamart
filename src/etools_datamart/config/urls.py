from django.conf import settings
from django.contrib.admin import site
from django.urls import include, path, re_path

from django_sysinfo.views import admin_sysinfo, http_basic_login, sysinfo, version
from oauth2_provider.views import AuthorizationView

import etools_datamart.api.urls
from etools_datamart.apps.multitenant.views import SelectSchema

urlpatterns = [
    path(r'me/', include('etools_datamart.apps.me.urls')),
    path(r's/', include('etools_datamart.apps.subscriptions.urls')),
    path(r'', include('etools_datamart.apps.web.urls')),
    path(r'', include('social_django.urls', namespace='social')),

    re_path(r'^authorize/?$', AuthorizationView.as_view(), name="authorize"),
    path(r'api/', include(etools_datamart.api.urls), name='api'),

    path(r'admin/', site.urls),
    path(r'admin/schemas/', SelectSchema.as_view(), name='select-schema'),
    path(r'admin/sysinfo/', admin_sysinfo, name="sys-admin-info"),
    path(r'impersonate/', include('impersonate.urls')),

    path(r'sys/info/', http_basic_login(sysinfo), name='sys-info'),
    path(r'sys/version/<name>/', http_basic_login(version), name='sys-version'),

]

urlpatterns = [
    path(settings.URL_PREFIX, include(urlpatterns)),
]
