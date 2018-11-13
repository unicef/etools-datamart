from django.contrib.auth.views import LogoutView
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, 'index.html')


class DisconnectView(LogoutView):
    def get_next_page(self):
        return 'https://login.microsoftonline.com/unicef.org/oauth2/logout?post_logout_redirect_uri=https://datamart.unicef.io/'
