import codecs
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import path

from etools_datamart.apps.subscriptions.views import subscribe


def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if "HTTP_AUTHORIZATION" in request.META:
            authmeth, auth = request.META["HTTP_AUTHORIZATION"].split(" ", 1)
            if authmeth.lower() == "basic":
                auth = codecs.decode(auth.encode("utf8").strip(), "base64").decode()
                username, password = auth.split(":", 1)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')
                else:
                    return HttpResponse(status=401)
        return func(request, *args, **kwargs)

    return _decorator


def http_basic_login(func):
    return http_basic_auth(login_required(func))


urlpatterns = [
    path(r'subscribe/<etl_id>/', http_basic_login(subscribe), name='subscribe'),
]
