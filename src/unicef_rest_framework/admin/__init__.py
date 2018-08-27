# -*- coding: utf-8 -*-
from django.contrib import admin

from .base import APIModelAdmin  # noqa
from .filter import SystemFilterAdmin
from ..models import (Application,
                      Service,
                      CacheVersion,
                      UserAccessControl,
                      SystemFilter)
from .base import ListDisplayAllMixin, ReadOnlyModelAdmin, TruncateTableMixin  # noqa
from .application import ApplicationAdmin
from .service import ServiceAdmin
from .cache import CacheVersionAdmin
from .acl import UserACLAdmin

__all__ = ['ApplicationAdmin',
           'CacheVersionAdmin'
           'GroupACLAdmin',
           'ServiceAdmin',
           'UserACLAdmin',
           'ListDisplayAllMixin',
           'ReadOnlyModelAdmin']

admin.site.register(Application, ApplicationAdmin)
admin.site.register(CacheVersion, CacheVersionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(UserAccessControl, UserACLAdmin)
admin.site.register(SystemFilter, SystemFilterAdmin)
