from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.template.response import TemplateResponse

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.config.settings import env


def index(request):
    context = {'page': 'index'}
    return TemplateResponse(request, 'index.html', context)


@login_required
def monitor(request):
    context = {'tasks': EtlTask.objects.all(),
               'subscriptions': request.user.subscriptions,
               'page': 'monitor'}
    return TemplateResponse(request, 'monitor.html', context)


class DisconnectView(LogoutView):
    def get_next_page(self):  # pragma: no cover
        return env('DISCONNECT_URL')
