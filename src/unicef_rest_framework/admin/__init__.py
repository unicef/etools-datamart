# -*- coding: utf-8 -*-
from django.contrib import admin

from unicef_rest_framework.models.acl import GroupAccessControl
from .base import APIModelAdmin  # noqa
from .filter import SystemFilterAdmin
from ..models import (Application,
                      Service,
                      CacheVersion,
                      UserAccessControl,
                      SystemFilter)
from .base import ListDisplayAllMixin, ReadOnlyAdminMixin, TruncateTableMixin  # noqa
from .application import ApplicationAdmin
from .service import ServiceAdmin
from .cache import CacheVersionAdmin
from .acl import UserAccessControlAdmin, GroupAccessControlAdmin

__all__ = ['ApplicationAdmin',
           'GroupAccessControlAdmin',
           'ServiceAdmin',
           'UserAccessControlAdmin',
           'ListDisplayAllMixin',
           'ReadOnlyAdminMixin']

admin.site.register(Application, ApplicationAdmin)
admin.site.register(CacheVersion, CacheVersionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(UserAccessControl, UserAccessControlAdmin)
admin.site.register(SystemFilter, SystemFilterAdmin)
admin.site.register(GroupAccessControl, GroupAccessControlAdmin)
