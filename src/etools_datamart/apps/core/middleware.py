# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import threading

from etools_datamart.state import state

logger = logging.getLogger(__name__)

_thread_locals = threading.local()


class ApiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        schema = request.META.get('HTTP_X_SCHEMA', "")
        # conn = connections['etools']
        # conn.set_schema(schema)

        state.request = request
        state.schemas = schema.split(',')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
