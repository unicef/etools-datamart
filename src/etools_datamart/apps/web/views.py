from django.contrib.auth.views import LogoutView
from django.template.response import TemplateResponse

from etools_datamart.config.settings import env


def index(request):
    return TemplateResponse(request, 'index.html')


class DisconnectView(LogoutView):
    def get_next_page(self):  # pragma: no cover
        return env('DISCONNECT_URL')
