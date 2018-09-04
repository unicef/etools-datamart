# -*- coding: utf-8 -*-
import logging

from coreapi.compat import urlparse
from drf_yasg.app_settings import swagger_settings
from drf_yasg.errors import SwaggerGenerationError
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.schemas import SchemaGenerator

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
