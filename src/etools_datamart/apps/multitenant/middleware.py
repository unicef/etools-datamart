# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import threading

from django.http import HttpResponseRedirect
from django.urls import reverse

from etools_datamart.state import state

logger = logging.getLogger(__name__)

_thread_locals = threading.local()


def _get_schemas(request):
    if '_schemas' in request.GET:
        return request.GET['_schemas']
    elif 'HTTP_X_SCHEMA' in request.META:
        return request.META.get('HTTP_X_SCHEMA')
    else:
        return request.COOKIES.get('schemas')


class MultiTenantMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        schemas = _get_schemas(request)
        if not schemas:
            # TODO: this redirect make sense only in "HTML" mode
            # it should be moved in AdminSite (and maybe BrowseableAPI)
            if request.path.startswith('/admin/'):
                if request.user and request.user.is_authenticated:
                    select_schema_url = reverse('select-schema')
                    if request.path != select_schema_url:
                        return HttpResponseRedirect(select_schema_url)
            state.schemas = []
        else:
            state.schemas = schemas.split(',')
        state.request = request
        response = self.get_response(request)
        response.set_cookie('schemas', ",".join(state.schemas))

        return response
