# -*- coding: utf-8 -*-
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
        state.request = request
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        response['system-filter'] = getattr(state.request, '_system_filter', '')
        response['cache-key'] = state.get('cache-key')
        response['cache-hit'] = state.get('cache-hit')
        response['cache-ttl'] = state.get('cache-ttl')
        response['cache-version'] = state.get('cache-version')
        return response
