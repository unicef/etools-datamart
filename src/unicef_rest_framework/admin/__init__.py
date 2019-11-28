# -*- coding: utf-8 -*-
from django.contrib import admin

from django_celery_beat.models import CrontabSchedule

from unicef_rest_framework.admin.export import ExportAdmin
from unicef_rest_framework.admin.preload import PreloadAdmin
from unicef_rest_framework.models import Preload
from unicef_rest_framework.models.acl import GroupAccessControl

from .. import models
from .acl import GroupAccessControlAdmin, UserAccessControlAdmin
from .application import ApplicationAdmin
from .base import ListDisplayAllMixin, ReadOnlyAdminMixin, TruncateTableMixin  # noqa
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
admin.site.register(models.PeriodicTask, PeriodicTaskAdmin)
admin.site.register(CrontabSchedule, CrontabScheduleAdmin)

admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.CacheVersion, CacheVersionAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.UserAccessControl, UserAccessControlAdmin)
admin.site.register(models.SystemFilter, SystemFilterAdmin)
admin.site.register(GroupAccessControl, GroupAccessControlAdmin)
admin.site.register(Preload, PreloadAdmin)
admin.site.register(models.Export, ExportAdmin)
