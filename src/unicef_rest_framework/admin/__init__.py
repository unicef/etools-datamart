# -*- coding: utf-8 -*-
from django.contrib import admin

from .base import APIModelAdmin  # noqa
from .filter import SystemFilterAdmin
from ..models import (Application,
                      Service,
                      CacheVersion,
                      UserAccessControl,
                      SystemFilter,
                      Category)
from .base import ListDisplayAllMixin, ReadOnlyModelAdmin, TruncateTableMixin  # noqa
from .application import ApplicationAdmin
from .service import ServiceAdmin
from .cache import CacheVersionAdmin
from .category import CategoryAdmin
from .acl import (ApplicationACLAdmin,
                  UserACLAdmin,
                  GroupACLAdmin)

__all__ = ['ApplicationAdmin',
           'CacheVersionAdmin'
           'CategoryAdmin',
           'GroupACLAdmin',
           'ApplicationACLAdmin',
           'ServiceAdmin',
           'UserACLAdmin',
           'ListDisplayAllMixin',
           'ReadOnlyModelAdmin']

admin.site.register(Application, ApplicationAdmin)
admin.site.register(CacheVersion, CacheVersionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(UserAccessControl, UserACLAdmin)
admin.site.register(SystemFilter, SystemFilterAdmin)
