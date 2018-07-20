from django.conf.urls import include
from django.contrib.admin import site
from django.urls import re_path
from django.views.generic import TemplateView

import etools_datamart.api.urls

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(), name='home'),
    re_path(r'^api/', include(etools_datamart.api.urls), name='api'),
    re_path('^admin/', site.urls),

]
