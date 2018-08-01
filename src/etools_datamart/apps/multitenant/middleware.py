# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import threading

from django.http import HttpResponseRedirect
from django.urls import reverse

from etools_datamart.state import state

logger = logging.getLogger(__name__)

_thread_locals = threading.local()


class MultiTenantMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        select_schema_url = reverse('multitenant:select-schema')
        if request.user and request.user.is_authenticated:
            schemas = request.COOKIES.get('schemas', request.META.get('HTTP_X_SCHEMA', ""))
            if not schemas:
                if request.path != select_schema_url:
                    return HttpResponseRedirect(select_schema_url)
            state.schemas = schemas.split(',')

        state.request = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
