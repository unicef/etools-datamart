# -*- coding: utf-8 -*-
from django.template.defaultfilters import pluralize

from rest_framework.exceptions import PermissionDenied


class InvalidSchema(Exception):
    def __init__(self, *schema):
        self.schema = schema

    def __str__(self):
        return "Invalid schema%s: %s" % (pluralize(self.schema),
                                         ','.join(self.schema))


class NotAuthorizedSchema(PermissionDenied):
    def __init__(self, schema, *args, **kwargs):
        self.schema = schema

    def __str__(self):
        return f"You are not allowed to access schema: '{self.schema}'"
