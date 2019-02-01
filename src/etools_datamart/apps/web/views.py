from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.template.response import TemplateResponse

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.config.settings import env


def index(request):
    context = {'page': 'index', 'title': 'eTools Datamart'}
    return TemplateResponse(request, 'index.html', context)


@login_required
def monitor(request):
    context = {'tasks': EtlTask.objects.all(),
               'subscriptions': request.user.subscriptions,
               'page': 'monitor'}
    return TemplateResponse(request, 'monitor.html', context)


def whoami(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.email)
    return HttpResponse('')


class DisconnectView(LogoutView):
    def get_next_page(self):  # pragma: no cover
        return env('DISCONNECT_URL')


class DatamartLoginView(LoginView):

    def get_context_data(self, **kwargs):
        kwargs['settings'] = settings
        return super().get_context_data(**kwargs)
