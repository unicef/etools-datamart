import logging

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connections

logger = logging.getLogger(__name__)


# class SQLStatementValidator(BaseValidator):
#     message = 'Ensure this value is valid SQL clause.'
#     code = 'sql'
#
#     def __call__(self, value):
#         try:
#             parts = sqlparse.parse(value)
#             tokens = parts[0].tokens
#             dml = [token for token in tokens if token.ttype is Keyword.DML]
#             if not dml or dml[0].value != 'SELECT':
#                 raise ValidationError("Only SELECT statement allowed", code=self.code)
#
#         except SQLParseError:
#             raise ValidationError(self.message, code=self.code)


# class SQLForm(forms.Form):
#     raw = forms.BooleanField(required=False)
#     statement = forms.CharField(widget=forms.Textarea,
#                                 validators=[SQLStatementValidator("")])
#     original = forms.CharField(widget=forms.Textarea,
#                                required=False,
#                                validators=[SQLStatementValidator("")])
#
#     def __init__(self, *args, **kwargs):
#         self.confirm = kwargs.pop('confirm', False)
#         super().__init__(*args, **kwargs)
#         if self.confirm:
#             self.fields['raw'].widget = forms.HiddenInput()
#             self.fields['raw'].original = forms.HiddenInput()
#
#     @property
#     def media(self):
#         extra = '' if settings.DEBUG else '.min'
#         js = [
#             'vendor/jquery/jquery%s.js' % extra,
#             'jquery.init.js',
#         ]
#         return forms.Media(js=['admin/js/%s' % url for url in js])


class SchemasForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        schemas = connections['etools'].get_tenants()
        for schema in schemas:
            self.fields[schema.schema_name] = forms.BooleanField(
                label=schema.name,
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
