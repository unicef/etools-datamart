# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict
from functools import lru_cache

import coreapi
import coreschema
from django import forms
from django.db import models
from django.template import loader
from django.utils.encoding import force_text
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework.filters import BaseFilterBackend
from unicef_rest_framework.models import SystemFilter

logger = logging.getLogger(__name__)


class SystemFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filters = {}
        if request.user and request.user.is_authenticated:
            filters['user'] = request.user
        else:
            return queryset

        filters['service'] = view.get_service()

        filter = SystemFilter.objects.match(request, view)
        if filter:
            queryset = filter.filter_queryset(queryset)
            request._request._system_filter = filter.get_querystring()
        return queryset


SCHEMAMAP = {
    models.BooleanField: coreschema.Boolean,
    models.IntegerField: coreschema.Integer,
    models.DecimalField: coreschema.Number,
    # models.DateField: coreschema.Anything,
}


class CoreAPIQueryStringFilterBackend(QueryStringFilterBackend):
    form_prefix = ""
    template = "querystringfilter/filter.html"

    def get_form_class(self, request, view):
        fields = OrderedDict([
            (name, forms.CharField(required=False))
            for name in view.filter_fields])

        return type(str('%sForm' % self.__class__.__name__),
                    (forms.Form,), fields)

    def get_form(self, request, view):
        if not hasattr(self, '_form'):
            Form = self.get_form_class(request, view)
            self._form = Form(request.GET, prefix=self.form_prefix)
        return self._form

    def to_html(self, request, queryset, view):
        template = loader.get_template(self.template)
        context = {'form': self.get_form(request, view)}
        return template.render(context, request)

    @lru_cache(100)
    def get_schema_fields(self, view):
        ret = []
        for field in view.filter_fields:
            model = view.serializer_class.Meta.model
            model_field = model._meta.get_field(field)
            coreapi_type = SCHEMAMAP.get(type(model_field), coreschema.String)
            ret.append(coreapi.Field(
                name=field,
                required=False,
                location='query',
                schema=coreapi_type(
                    title=force_text(field),
                    description=f'{model_field.help_text} - django queryset syntax allowed'
                )
            ))
        return ret
