# -*- coding: utf-8 -*-
import logging

from rest_framework.renderers import BrowsableAPIRenderer as _BrowsableAPIRenderer

logger = logging.getLogger(__name__)


class APIBrowsableAPIRenderer(_BrowsableAPIRenderer):
    template = 'rest_framework/api.html'
