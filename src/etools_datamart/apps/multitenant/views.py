# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from etools_datamart.apps.multitenant.forms import SchemasForm

logger = logging.getLogger(__name__)


class SelectSchema(FormView):
    template_name = 'schemas.html'
    form_class = SchemasForm
    success_url = reverse_lazy("admin:index")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = ""

    def get_form(self, form_class=None):
        return super().get_form(form_class)

    def get_initial(self):
        self.selected = self.request.COOKIES.get('schemas', '')
        return {k: True for k in self.selected.split(',')}

    def get_success_url(self):
        if 'from' in self.request.GET:
            return self.request.GET['from']
        return super().get_success_url()

    def form_valid(self, form):
        self.selected = ",".join([k for (k, v) in form.cleaned_data.items() if v])
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie('schemas', self.selected)
        return response

    def render_to_response(self, context, **response_kwargs):
        # self.selected = self.request.COOKIES.get('schemas', '')
        response = super().render_to_response(context, **response_kwargs)
        return response
