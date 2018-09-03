from django.contrib.admin import site
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django_sysinfo.views import admin_sysinfo, http_basic_login, sysinfo, version

import etools_datamart.api.urls

urlpatterns = [
    path(r'login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path(r'logout/', auth_views.logout, {'next_page': '/'}, name='logout'),

    path(r'', include('etools_datamart.apps.multitenant.urls')),
    path(r'', TemplateView.as_view(template_name='index.html'), name='home'),
    path(r'api/', include(etools_datamart.api.urls), name='api'),
    path('admin/', site.urls),

    path('sys/info/', http_basic_login(sysinfo), name='sys-info'),
    re_path('sys/version/(?P<name>.*)/', http_basic_login(version), name='sys-version'),
    path("admin/sysinfo/", admin_sysinfo, name="sys-admin-info"),

]
