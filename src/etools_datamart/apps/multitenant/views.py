# -*- coding: utf-8 -*-
import logging

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connections
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

logger = logging.getLogger(__name__)


class SchemasForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        schemas = connections['etools'].get_tenants()
        for schema in schemas:
            self.fields[schema.schema_name] = forms.BooleanField(
                label=schema.name,
                # label=f"{schema.name} - {schema.schema_name}",
                required=False)

    def clean(self):
        selected = [(k, v) for (k, v) in self.cleaned_data.items() if v]
        if not selected:
            raise ValidationError("Select at least one workspace")
        return super().clean()

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        js = [
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
        ]
        return forms.Media(js=['admin/js/%s' % url for url in js])


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

    def form_valid(self, form):
        self.selected = ",".join([k for (k, v) in form.cleaned_data.items() if v])
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie('schemas', self.selected)
        return response

    def render_to_response(self, context, **response_kwargs):
        # self.selected = self.request.COOKIES.get('schemas', '')
        response = super().render_to_response(context, **response_kwargs)
        return response
