import logging

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# from unicef_rest_framework.state import state
from unicef_rest_framework.utils import get_query_string

from etools_datamart.apps.multitenant.forms import SchemasForm

logger = logging.getLogger(__name__)


class SelectSchema(FormView):
    template_name = 'schemas.html'
    form_class = SchemasForm
    success_url = reverse_lazy("admin:index")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = []

    def get_initial(self):
        self.params = dict(self.request.GET.items())

        # self.selected = self.request.COOKIES.get('schemas', '').split(",")
        self.selected = self.params.get('country_name', "").split(",")

        return {k: True for k in self.selected}

    def get_success_url(self):
        self.params = dict(self.request.GET.items())
        _from = self.request.GET.getlist('from', ['/'])[0]
        if '_all' in self.selected:
            qs = self.get_query_string({}, ['from', 'country_name'])
        else:
            qs = self.get_query_string({'country_name': ','.join(self.selected)}, ['from'])
        return f"{_from}{qs}"

    def form_valid(self, form):
        self.selected = [k for (k, v) in form.cleaned_data.items() if v]
        if len(self.selected) == len(form.cleaned_data):
            self.selected = ['_all']

        response = HttpResponseRedirect(self.get_success_url())
        # state.schemas = self.selected
        # response.set_cookie('schemas', ','.join(self.selected))
        return response

    def get_query_string(self, new_params=None, remove=None):
        return get_query_string(self.params, new_params, remove)
        # if new_params is None:
        #     new_params = {}
        # if remove is None:
        #     remove = []
        # p = self.params.copy()
        # for r in remove:
        #     for k in list(p):
        #         if k.startswith(r):
        #             del p[k]
        # for k, v in new_params.items():
        #     if v is None:
        #         if k in p:
        #             del p[k]
        #     else:
        #         p[k] = v
        # return '?%s' % urlencode(sorted(p.items()))
