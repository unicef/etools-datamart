# -*- coding: utf-8 -*-
from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import ReferenceResolver
from drf_yasg.utils import get_consumes, get_produces
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.settings import api_settings as rest_framework_settings


class APISchemaGenerator(OpenAPISchemaGenerator):

    def get_schema(self, request=None, public=False):
        endpoints = self.get_endpoints(request)
        components = ReferenceResolver(openapi.SCHEMA_DEFINITIONS)
        self.consumes = get_consumes(rest_framework_settings.DEFAULT_PARSER_CLASSES)
        self.produces = get_produces(rest_framework_settings.DEFAULT_RENDERER_CLASSES)
        paths, prefix = self.get_paths(endpoints, components, request, public)

        security_definitions = swagger_settings.SECURITY_DEFINITIONS
        if security_definitions is not None:
            security_definitions = OrderedDict(sorted([(key, OrderedDict(sorted(sd.items())))
                                                       for key, sd in swagger_settings.SECURITY_DEFINITIONS.items()]))
        security_requirements = swagger_settings.SECURITY_REQUIREMENTS
        if security_requirements is None:
            security_requirements = [{security_scheme: []} for security_scheme in swagger_settings.SECURITY_DEFINITIONS]

        security_requirements = sorted(security_requirements, key=lambda od: list(sorted(od)))
        security_requirements = [OrderedDict(sorted(sr.items())) for sr in security_requirements]

        url = self.url
        if url is None and request is not None:
            url = request.build_absolute_uri()

        return openapi.Swagger(
            info=self.info, paths=paths, consumes=self.consumes or None, produces=self.produces or None,
            security_definitions=security_definitions, security=security_requirements,
            _url=url, _prefix=prefix, _version=self.version, **dict(components)
        )


description = """
Welcome to eTools Datamart API
------------------------------

Here wou can find us...

"""
schema_view = get_schema_view(
    openapi.Info(
        title="eTools Datamart API",
        default_version='v1',
        description=description,
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
        aaaaaaa="aaaaaa",

    ),
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=APISchemaGenerator
)
