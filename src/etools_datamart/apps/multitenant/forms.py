# -*- coding: utf-8 -*-
import logging

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connections

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
