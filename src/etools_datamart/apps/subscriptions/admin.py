from django.contrib import admin
from django.contrib.admin import register

from admin_extra_urls.mixins import ExtraUrlMixin

from . import models


@register(models.Subscription)
class SubscriptionAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ('user', 'content_type', 'type')
    list_filter = ('user', 'content_type', 'type')
