import random
import string

from django.contrib.auth import BACKEND_SESSION_KEY, login
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def generate(self, length=20):
        pwd = ""
        count = 0
        length = max(8, length)
        while count < length:
            upper = [random.choice(string.ascii_uppercase)]
            lower = [random.choice(string.ascii_lowercase)]
            num = [random.choice(string.digits)]
            symbol = [random.choice(string.punctuation)]
            everything = upper + lower + num + symbol
            pwd += random.choice(everything)
            count += 1
            if count >= length:
                break
        return pwd

    def get_context_data(self, **kwargs):
        kwargs.update({'page': 'profile',
                       'business_areas': sorted(get_allowed_schemas(self.request.user)),
                       'services': get_allowed_services(self.request.user),
                       'user': self.request.user
                       })
        return super().get_context_data(**kwargs)

    def get_initial(self):
        return {
        }

    # def get_success_url(self):
    #     return self.request.path

    def form_valid(self, form):
        ctx = self.get_context_data(form=form)
        if self.request.user.is_authenticated:
            pwd = self.generate()
            self.request.user.set_password(pwd)
            self.request.user.save()
            ctx['password'] = pwd
            login(self.request, self.request.user, self.request.session[BACKEND_SESSION_KEY])
        return self.render_to_response(ctx)
