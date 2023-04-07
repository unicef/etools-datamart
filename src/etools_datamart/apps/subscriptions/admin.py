from django.contrib import admin
from django.contrib.admin import register

from admin_extra_buttons.mixins import ExtraButtonsMixin

from . import models


@register(models.Subscription)
class SubscriptionAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ("user", "content_type", "type")
    list_filter = ("user", "content_type", "type")
