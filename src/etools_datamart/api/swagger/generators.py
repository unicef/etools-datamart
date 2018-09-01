# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

from coreapi.compat import urlparse
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.errors import SwaggerGenerationError
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import ReferenceResolver
from drf_yasg.utils import get_consumes, get_produces
from rest_framework.schemas import SchemaGenerator
from rest_framework.settings import api_settings as rest_framework_settings

logger = logging.getLogger(__name__)


class APISchemaGenerator(OpenAPISchemaGenerator):

    def __init__(self, info, version='', url=None, patterns=None, urlconf=None):
        if url is None and swagger_settings.DEFAULT_API_URL is not None:
            url = swagger_settings.DEFAULT_API_URL

        if url:
            parsed_url = urlparse.urlparse(url)
            if parsed_url.scheme not in ('http', 'https') or not parsed_url.netloc:
                raise SwaggerGenerationError("`url` must be an absolute HTTP(S) url")
            if parsed_url.path:
                logger.warning("path component of api base URL %s is ignored; use FORCE_SCRIPT_NAME instead" % url)

        info.description = info.description.format(HOST=url)

        self._gen = SchemaGenerator(info.title, url, info.get('description', ''), patterns, urlconf)
        self.info = info
        self.version = version
        self.consumes = []
        self.produces = []

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
