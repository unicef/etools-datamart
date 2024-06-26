import json
import logging
from urllib.parse import urlencode

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.defaultfilters import pluralize
from django.urls import reverse
from django.utils.safestring import mark_safe

from admin_extra_buttons.decorators import button

from unicef_rest_framework.admin import APIModelAdmin, TruncateTableMixin
from unicef_rest_framework.utils import humanize_size

from etools_datamart.libs.admin_filters import SizeFilter, TimeFilter

from .models import APIRequestLog, DailyCounter, MonthlyCounter, PathCounter, UserCounter

logger = logging.getLogger(__name__)


class APIRequestLogAdmin(TruncateTableMixin, admin.ModelAdmin):
    date_hierarchy = "requested_at"
    search_fields = ("path", "user__username")
    list_display = (
        "requested_at",
        "response_ms",
        "size",
        "requestor",
        "method",
        "url",
        "content_type",
        "cached",
        "is_filtered",
    )
    list_filter = ("cached", "content_type", SizeFilter, TimeFilter)
    readonly_fields = (
        "user",
        "path",
        "requested_at",
        "response_ms",
        "size",
        "method",
        "cached",
        "remote_addr",
        "response_length",
        "query_params",
        "data",
        "content_type",
        "viewset",
        "service",
    )

    fieldsets = (
        (
            "",
            {
                "fields": (
                    (
                        "requested_at",
                        "user",
                    ),
                )
            },
        ),
        (
            "Response",
            {
                "classes": ("grp-collapse grp-open",),
                "fields": (
                    ("content_type", "response_length", "response_ms", "cached"),
                    ("viewset", "service"),
                ),
            },
        ),
        (
            "Request",
            {
                "classes": ("grp-collapse grp-open",),
                "fields": (
                    ("remote_addr", "method", "path"),
                    "query_params",
                    "data",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    @button(icon="fa fa-compress icon-white")
    def aggregate(self, request):
        processed = APIRequestLog.objects.aggregate()
        self.message_user(request, "{} {} aggregated".format(processed, pluralize(processed, "day,days")))

    @button()
    def preload(self, request, pk):
        obj = APIRequestLog.objects.get(id=pk)
        from unicef_rest_framework.models import Preload

        Preload.objects.get_or_create(url=obj.path, params=json.loads(obj.query_params), as_user=obj.user)
        base_url = reverse("admin:unicef_rest_framework_preload_changelist")
        return HttpResponseRedirect(base_url)

    def is_filtered(self, obj):
        return obj.query_params != "{}"

    is_filtered.boolean = True

    def url(self, obj):
        try:
            params = json.loads(obj.query_params)
        except ValueError:
            params = {}
        if params:
            html = "<a target='capi' href='{0.path}?{1}'>{0.path}</a>".format(obj, urlencode(params))
        else:
            html = "<a target='capi' href='{0.path}'>{0.path}</a>".format(obj)
        return mark_safe(html)

    url.admin_order_field = "path"
    url.allow_tags = True

    def requestor(self, obj):
        return obj.user

    # def event(self, obj):
    #     return obj.requested_at.strftime("<nobr>%Y-%m-%d %H:%M:%S</nobr>")
    #
    # event.admin_order_field = 'requested_at'
    # event.short_description = 'DateTime'
    # event.allow_tags = True

    def size(self, obj):
        return mark_safe("<nobr>{0}</nobr>".format(humanize_size(obj.response_length)))

    size.admin_order_field = "response_length"
    size.allow_tags = True


class DailyCounterAdmin(TruncateTableMixin, APIModelAdmin):
    date_hierarchy = "day"
    editing = True


class MonthlyCounterAdmin(TruncateTableMixin, APIModelAdmin):
    date_hierarchy = "day"
    editing = True


class PathCounterAdmin(TruncateTableMixin, APIModelAdmin):
    date_hierarchy = "day"
    search_fields = ("path",)
    list_display = ("day", "path", "total", "cached", "response_max", "response_min", "response_average")


class UserCounterAdmin(TruncateTableMixin, APIModelAdmin):
    date_hierarchy = "day"
    list_display = ("day", "user", "total", "cached", "response_max", "response_min", "response_average")


class ApplicationCounterAdmin(TruncateTableMixin, APIModelAdmin):
    date_hierarchy = "day"


admin.site.register(APIRequestLog, APIRequestLogAdmin)
admin.site.register(MonthlyCounter, MonthlyCounterAdmin)
admin.site.register(DailyCounter, DailyCounterAdmin)
admin.site.register(PathCounter, PathCounterAdmin)
admin.site.register(UserCounter, UserCounterAdmin)
