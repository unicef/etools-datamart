from django.conf.urls import include
from django.contrib.admin import site
from django.urls import re_path, path
from django.views.generic import TemplateView

import etools_datamart.api.urls

urlpatterns = [
    path(r'', include('etools_datamart.apps.multitenant.urls')),
    path(r'', TemplateView.as_view(template_name='index.html'), name='home'),
    path(r'api/', include(etools_datamart.api.urls), name='api'),
    path('admin/', site.urls),

]
