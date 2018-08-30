# -*- coding: utf-8 -*-
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class APISchemaGenerator(OpenAPISchemaGenerator):
    pass


schema_view = get_schema_view(
    openapi.Info(
        title="eTools Datamart API",
        default_version='v1',
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=APISchemaGenerator
)
