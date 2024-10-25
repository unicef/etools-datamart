from functools import lru_cache, reduce

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import CreateView, DetailView, UpdateView

import rest_framework_extensions.utils
from django_filters.views import FilterView
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.reverse import reverse
from rest_framework.utils.breadcrumbs import get_breadcrumbs
from rest_framework_xml.renderers import XMLRenderer
from sentry_sdk import capture_exception
from strategy_field.utils import fqn

from unicef_rest_framework.forms import ExportForm
from unicef_rest_framework.models import Export
from unicef_rest_framework.models.export import ExportAccessLog, storage
from unicef_rest_framework.pagination import PageFilter
from unicef_rest_framework.utils import get_query_string, parse_url

from . import acl
from .auth import AnonymousAuthentication, basicauth, IPBasedAuthentication, JWTAuthentication, URLTokenAuthentication
from .cache import cache_response, etag, ListKeyConstructor
from .ds import DynamicSerializerFilter, DynamicSerializerMixin
from .filtering import ExportFilter, SystemFilterBackend
from .negotiation import CT
from .ordering import OrderingFilter
from .permissions import ServicePermission
from .renderers import (
    CSVRenderer,
    HTMLRenderer,
    IQYRenderer,
    JSONRenderer,
    MSJSONRenderer,
    MSXmlRenderer,
    PDFRenderer,
    TextRenderer,
    URFBrowsableAPIRenderer,
    XLSXRenderer,
    YAMLRenderer,
)


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class URFReadOnlyModelViewSet(DynamicSerializerMixin, viewsets.ReadOnlyModelViewSet):
    serializer_field_param = "-serializer"
    dynamic_fields_param = "+fields"

    object_cache_key_func = rest_framework_extensions.utils.default_object_cache_key_func
    list_cache_key_func = ListKeyConstructor()

    object_etag_func = rest_framework_extensions.utils.default_object_etag_func
    list_etag_func = ListKeyConstructor()

    authentication_classes = (
        SessionAuthentication,
        IPBasedAuthentication,
        TokenAuthentication,
        JWTAuthentication,
        BasicAuthentication,
        TokenAuthentication,
        IPBasedAuthentication,
        URLTokenAuthentication,
        AnonymousAuthentication,
    )
    default_access = acl.ACL_ACCESS_LOGIN
    content_negotiation_class = CT
    filter_backends = [QueryStringFilterBackend, OrderingFilter, DynamicSerializerFilter]

    renderer_classes = [
        JSONRenderer,
        URFBrowsableAPIRenderer,
        CSVRenderer,
        YAMLRenderer,
        XLSXRenderer,
        HTMLRenderer,
        PDFRenderer,
        MSJSONRenderer,
        XMLRenderer,
        MSXmlRenderer,
        TextRenderer,
        IQYRenderer,
    ]
    ordering_fields = ("id",)
    ordering = "id"
    filter_blacklist = []
    filter_fields = []
    # pagination_class = paginator()
    permission_classes = [
        ServicePermission,
    ]
    serializers_fieldsets = {}

    def get_filter_backends(self):
        #
        flt = list(self.filter_backends)
        if SystemFilterBackend not in flt:
            flt.insert(0, SystemFilterBackend)
        if PageFilter not in flt:
            flt.append(PageFilter)
        return flt

    def filter_queryset(self, queryset):
        # overridden to use get_filter_backends()
        for backend in self.get_filter_backends():
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def store(self, key, value):
        self.request._request.api_info[key] = value

    @transaction.non_atomic_requests
    def dispatch(self, request, *args, **kwargs):
        request._view = self
        if hasattr(request, "api_info"):
            request.api_info["view"] = fqn(self)
            request.api_info["service"] = self.get_service()

        return super().dispatch(request, *args, **kwargs)

    @classproperty
    def label(cls):
        return cls.__name__.replace("ViewSet", "")

    @classmethod
    @lru_cache()
    def get_service(cls):
        from unicef_rest_framework.models import Service

        return Service.objects.get_for_viewset(cls)

    @etag(etag_func="list_etag_func")
    @cache_response(key_func="list_cache_key_func", cache="api")
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)

    @etag(etag_func="object_etag_func")
    @cache_response(key_func="object_cache_key_func", cache="api")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @etag(etag_func="list_etag_func")
    @cache_response(key_func="list_cache_key_func", cache="api")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)


class ExportList(FilterView):
    model = Export
    filterset_class = ExportFilter


@method_decorator(basicauth, "dispatch")
class ExportFetch(LoginRequiredMixin, DetailView):
    model = Export

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        if record.check_access(request.user):
            try:
                c = storage.open(record.file_id)
                current_username = request.user.username
                ExportAccessLog.log_access(record, current_username)
            except FileNotFoundError as e:
                capture_exception(e)
                return JsonResponse({"error": "File not found"}, status=404)

            response = StreamingHttpResponse(c, status=200, content_type=record.format)
            if record.save_as or record.format != "application/json":
                response["Content-Disposition"] = 'attachment; filename="%s"' % record.filename
            return response
        return JsonResponse({"error": "Permission denied"}, status=403)


class ExportObjectMixin(LoginRequiredMixin):
    model = Export
    form_class = ExportForm

    def get_success_url(self):
        return reverse("urf:export-list")

    def form_valid(self, form):
        form.instance.as_user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        url = self.request.GET.get("url")
        path, params = parse_url(url)
        qs = get_query_string(params, remove=["page_size", "format"])
        data.update(
            {
                "breadcrumblist": self.breadcrumbs,
                "url": url,
                "source": "{}{}{}".format(settings.ABSOLUTE_BASE_URL, path, qs),
                "path": path,
                "qs": qs,
            }
        )
        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields.pop("enabled")
        return form


class ExportCreate(ExportObjectMixin, CreateView):
    def get_form_kwargs(self):
        path, params = parse_url(self.request.GET.get("url"), remove=["page_size"])
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "url": path,
                "params": params,
            }
        )
        return kwargs

    def get_initial(self):
        return {"name": self.breadcrumbs[-1][0], "filename": self.breadcrumbs[-1][0]}

    @cached_property
    def breadcrumbs(self):
        url = self.request.GET.get("url")
        return get_breadcrumbs(url, self.request)


class ExportUpdate(ExportObjectMixin, UpdateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"url": self.object.url})
        return kwargs

    def get_success_url(self):
        return reverse("urf:export-update", args=[self.object.id])

    @cached_property
    def breadcrumbs(self):
        url = self.object.get_full_url()
        return get_breadcrumbs(url, self.request)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        path, params = parse_url(self.object.url)
        qs = get_query_string(self.object.params, remove=["page_size", "format"])
        data.update(
            {
                "record": self.object,
                "url": self.object.get_full_url(),
                "path": path,
                "source": "{}{}{}".format(settings.ABSOLUTE_BASE_URL, path, qs),
                "qs": qs,
            }
        )
        return data
