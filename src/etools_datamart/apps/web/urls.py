from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.urls import path, re_path

import etools_datamart

from .views import DatamartLoginView, DisconnectView, index, monitor, whoami


def trigger_error(request):
    return 1 / 0


def healthcheck(request, version):
    if version == etools_datamart.VERSION:
        return JsonResponse({})
    return JsonResponse({}, status=404)


urlpatterns = [
    path(r"", index, name="home"),
    path("healthcheck/<str:version>/", healthcheck, name="healthcheck"),
    path(r"monitor/", monitor, name="monitor"),
    path(r"login/", DatamartLoginView.as_view(template_name="login.html"), name="login"),
    path(r"logout/", LogoutView.as_view(next_page="/"), name="logout"),
    # path(r'request-access/', RequestAccessView.as_view(), name='request-access'),
    # path(r'request-access/done/', RequestAccessDoneView.as_view(), name='request-access-done'),
    path(r"disconnect/", DisconnectView.as_view(next_page="/"), name="disconnect"),
    path(r"whoami/", whoami, name="whoami"),
    # path(r'password_reset/',
    #      auth_views.PasswordResetView.as_view(form_class=PasswordResetForm2), name='password_reset'),
    # path(r'password_reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    re_path(
        r"reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(r"reset/done/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_complete"),
    path("sentry-debug/", trigger_error),
]
