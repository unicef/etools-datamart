# -*- coding: utf-8 -*-
class InvalidSchema(Exception):
    def __init__(self, schema, *args, **kwargs):  # real signature unknown
        self.schema = schema

    def __str__(self):
        return f"Invalid schema: '{self.schema}'"


class NotAuthorizedSchema(InvalidSchema):
    def __init__(self, schema, *args, **kwargs):  # real signature unknown
        self.schema = schema

    def __str__(self):
        return f"You are not allowed to access schema: '{self.schema}'"
