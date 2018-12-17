import random
import string

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView

from etools_datamart.apps.etools.utils import get_allowed_schemas, get_allowed_services
from etools_datamart.apps.me.forms import ProfileForm


@login_required
def profile(request):
    context = {'form': ProfileForm()}
    return TemplateResponse(request, 'index.html', context)


class ProfileView(FormView):
    form_class = ProfileForm
    template_name = 'me/profile.html'

    def generate(self, length=20):
        pwd = ""
        count = 0
        while count != length:
            upper = [random.choice(string.ascii_uppercase)]
            lower = [random.choice(string.ascii_lowercase)]
            num = [random.choice(string.digits)]
            symbol = [random.choice(string.punctuation)]
            everything = upper + lower + num + symbol
            pwd += random.choice(everything)
            count += 1
            if count >= length:
                return pwd

    def get_context_data(self, **kwargs):
        kwargs.update({'page': 'profile',
                       'business_areas': get_allowed_schemas(self.request.user),
                       'services': get_allowed_services(self.request.user),
                       'user': self.request.user
                       })
        return super().get_context_data(**kwargs)

    def get_initial(self):
        return {
        }

    def form_valid(self, form):
        pwd = self.generate()
        ctx = self.get_context_data(form=form,
                                    password=pwd)
        return self.render_to_response(ctx)
