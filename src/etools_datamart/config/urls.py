from django.conf import settings
from django.contrib.admin import site
from django.urls import include, path, re_path

from oauth2_provider.views import AuthorizationView

import unicef_rest_framework.urls

import etools_datamart.api.urls
from etools_datamart.apps.multitenant.views import SelectSchema

urlpatterns = [
    path(r'me/', include('etools_datamart.apps.me.urls')),
    path(r's/', include('etools_datamart.apps.subscriptions.urls')),
    path(r'', include('etools_datamart.apps.web.urls')),
    path(r'', include('social_django.urls', namespace='social')),

    re_path(r'^authorize/?$', AuthorizationView.as_view(), name="authorize"),
    path(r'api/', include(etools_datamart.api.urls)),
    path(r'urf/', include(unicef_rest_framework.urls, namespace='urf')),

    path(r'admin/schemas/', SelectSchema.as_view(), name='select-schema'),
    path(r'admin/', site.urls),
    path(r'impersonate/', include('impersonate.urls')),
    path(r'explorer/', include('explorer.urls')),

]


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa


urlpatterns += [
    path('sentry-debug/', trigger_error),
]

urlpatterns = [
    path(settings.URL_PREFIX, include(urlpatterns)),
]
