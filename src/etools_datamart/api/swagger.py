# -*- coding: utf-8 -*-
import logging
from django.utils.translation import gettext as _
from drf_yasg.inspectors import CoreAPICompatInspector

logger = logging.getLogger(__name__)


class FilterInspector(CoreAPICompatInspector):
    pass
