# -*- coding: utf-8 -*-
from django.contrib import admin

from django_celery_beat.models import CrontabSchedule

from unicef_rest_framework.models.acl import GroupAccessControl

from ..models import Application, CacheVersion, PeriodicTask, Service, SystemFilter, UserAccessControl
from .acl import GroupAccessControlAdmin, UserAccessControlAdmin
from .application import ApplicationAdmin
from .base import ListDisplayAllMixin, ReadOnlyAdminMixin
from .beat import CrontabScheduleAdmin, PeriodicTaskAdmin
from .cache import CacheVersionAdmin
from .filter import SystemFilterAdmin
from .service import ServiceAdmin

from .base import APIModelAdmin  # noqa; noqa

__all__ = ['ApplicationAdmin',
           'GroupAccessControlAdmin',
           'ServiceAdmin',
           'UserAccessControlAdmin',
           'ListDisplayAllMixin',
           'ReadOnlyAdminMixin',
           'PeriodicTaskAdmin',
           'CrontabScheduleAdmin']

# admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.register(PeriodicTask, PeriodicTaskAdmin)
admin.site.register(CrontabSchedule, CrontabScheduleAdmin)

admin.site.register(Application, ApplicationAdmin)
admin.site.register(CacheVersion, CacheVersionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(UserAccessControl, UserAccessControlAdmin)
admin.site.register(SystemFilter, SystemFilterAdmin)
admin.site.register(GroupAccessControl, GroupAccessControlAdmin)
