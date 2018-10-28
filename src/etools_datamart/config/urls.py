from django.contrib.admin import site
from django.urls import include, path, re_path
from django_sysinfo.views import admin_sysinfo, http_basic_login, sysinfo, version

import etools_datamart.api.urls
from etools_datamart.apps.multitenant.views import SelectSchema

urlpatterns = [
    path(r'', include('etools_datamart.apps.web.urls')),
    path('', include('social_django.urls', namespace='social')),

    path(r'api/auth/', include('rest_framework_social_oauth2.urls')),
    path(r'api/', include(etools_datamart.api.urls), name='api'),

    path('admin/', site.urls),
    path(r'admin/schemas/', SelectSchema.as_view(), name='select-schema'),

    path('sys/info/', http_basic_login(sysinfo), name='sys-info'),
    re_path('sys/version/(?P<name>.*)/', http_basic_login(version), name='sys-version'),
    path("admin/sysinfo/", admin_sysinfo, name="sys-admin-info"),

]
