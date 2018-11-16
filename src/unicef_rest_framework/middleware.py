# -*- coding: utf-8 -*-
import logging
import threading

# from unicef_rest_framework.state import state

logger = logging.getLogger(__name__)

_thread_locals = threading.local()


class ApiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.api_info = {}
        response = self.get_response(request)

        response['filters'] = request.api_info.get('filters', '')
        response['excludes'] = request.api_info.get('excludes', '')
        response['system-filters'] = request.api_info.get('system-filter', '')
        response['cache-key'] = request.api_info.get('cache-key', '')
        response['cache-hit'] = request.api_info.get('cache-hit', '')
        response['cache-ttl'] = request.api_info.get('cache-ttl', '')
        response['cache-version'] = request.api_info.get('cache-version', '')
        return response
