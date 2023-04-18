from django import forms
from django.contrib.auth.models import Group
from django.db import connections
from django.forms import ModelForm

from .models import SchemaAccessControl

conn = connections["etools"]


class SchemaAccessControlForm(ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    schemas = forms.MultipleChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["schemas"].choices = zip(conn.all_schemas, conn.all_schemas)

    class Meta:
        model = SchemaAccessControl
        fields = ("group", "schemas")

    def clean_schemas(self):
        return sorted(self.cleaned_data["schemas"])
