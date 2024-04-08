from collections import OrderedDict

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import SimpleAdminConfig
from django.core.cache import caches
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views.decorators.cache import never_cache

from constance import config

from etools_datamart.libs.version import get_full_version

cache = caches["default"]

DEFAULT_INDEX_SECTIONS = {
    "Administration": ["unicef_rest_framework", "constance", "subscriptions", "etl"],
    "Data": ["data", "prp", "rapidpro"],
    "Source/eTools": ["etools"],
    "Source/PRP": ["source_prp"],
    "Security": [
        "auth",
        "core.User",
        "security",
        "unicef_rest_framework.GroupAccessControl",
        "unicef_rest_framework.UserAccessControl",
    ],
    "Logs": [
        "tracking",
    ],
    "System": ["django_celery_beat", "post_office", "unicef_rest_framework.PeriodicTask"],
    "Other": [],
    "_hidden_": [
        "sites",
        "unicef_rest_framework.Application",
        "oauth2_provider",
        "social_django",
        "django_celery_beat.PeriodicTask",
    ],
}


def reset_counters(request):
    from etools_datamart.apps.tracking.utils import reset_all_counters

    reset_all_counters()
    return HttpResponseRedirect("..")


def refresh_counters(request):
    from etools_datamart.apps.tracking.utils import refresh_all_counters

    refresh_all_counters()
    return HttpResponseRedirect("..")


class DatamartAdminSite(AdminSite):
    site_title = gettext_lazy("Datamart site admin")

    site_header = gettext_lazy("Datamart administration")

    def app_index(self, request, app_label, extra_context=None):
        if app_label == "tracking":
            from etools_datamart.apps.tracking.utils import get_all_counters

            extra_context = {"numbers": get_all_counters()}
        return super().app_index(request, app_label, extra_context)

    def get_urls(self):
        from django.urls import re_path

        urls = super().get_urls()
        urls = [
            re_path("tracking/reset/", self.admin_view(reset_counters), name="tracking-reset"),
            re_path("tracking/refresh/", self.admin_view(refresh_counters), name="tracking-refresh"),
        ] + urls
        return urls

    @method_decorator(never_cache)
    def index(self, request, extra_context=None):
        style = request.COOKIES.get("old_index_style", 0)
        if style in [1, "1"]:
            return super().index(request, {"index_style": 0})
        else:
            return self.index_new(request, {"index_style": 1})

    @method_decorator(never_cache)
    def index_new(self, request, extra_context=None):
        key = f"2apps_groups:{request.user.id}:{get_full_version()}:{config.CACHE_VERSION}"
        app_list = self.get_app_list(request)
        groups = cache.get(key)
        if not groups or not isinstance(groups, dict):
            sections = getattr(settings, "INDEX_SECTIONS", DEFAULT_INDEX_SECTIONS)
            groups = OrderedDict([(k, []) for k in sections.keys()])

            def get_section(model, app):
                fqn = "%s.%s" % (app["app_label"], model["object_name"])
                target = "Other"
                if fqn in sections["_hidden_"] or app["app_label"] in sections["_hidden_"]:
                    return "_hidden_"

                for sec, models in sections.items():
                    if fqn in models:
                        return sec
                    elif app["app_label"] in models:
                        target = sec
                return target

            for app in app_list:
                for model in app["models"]:
                    sec = get_section(model, app)
                    groups[sec].append(
                        {
                            "app_label": str(app["app_label"]),
                            "app_name": str(app["name"]),
                            "app_url": app["app_url"],
                            "label": "%s - %s" % (app["name"], model["object_name"]),
                            "model_name": str(model["name"]),
                            "admin_url": model["admin_url"],
                            "perms": model["perms"],
                        }
                    )
            for __, models in groups.items():
                models.sort(key=lambda x: x["label"])
            cache.set(key, groups, 60 * 60)

        context = {
            **self.each_context(request),
            # 'title': self.index_title,
            "app_list": app_list,
            "groups": dict(groups),
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, "admin/index_new.html", context)


class AdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default_site = "etools_datamart.config.admin.DatamartAdminSite"

    def ready(self):
        super().ready()
        self.module.autodiscover()
