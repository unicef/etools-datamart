from __future__ import absolute_import, unicode_literals

import logging
from collections import OrderedDict
from functools import lru_cache

from django import forms
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import BooleanField, FieldDoesNotExist
from django.template import loader
from django.utils.encoding import force_text

import coreapi
import coreschema
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from .exceptions import InvalidFilterError, InvalidQueryArgumentError, InvalidQueryValueError, QueryFilterException
from .filters import parse_bool, RexList

logger = logging.getLogger(__name__)

SCHEMAMAP = {
    models.BooleanField: coreschema.Boolean,
    models.IntegerField: coreschema.Integer,
    models.DecimalField: coreschema.Number,
    # models.DateField: coreschema.Anything,
}


class QueryStringFilterBackend(BaseFilterBackend):
    template = "querystringfilter/filter.html"
    form_prefix = ''
    allowed_joins = -1
    field_casting = {}

    def __init__(self) -> None:
        self.unknown_arguments = []

    def get_form_class(self, request, view):
        if hasattr(view, 'querystringfilter_form_class'):
            return view.querystringfilter_form_class
        fields = OrderedDict([
            (name, forms.CharField(required=False))
            for name in view.filter_fields or []])

        return type(str('%sForm' % self.__class__.__name__),
                    (forms.Form,), fields)

    def get_form(self, request, view):
        if hasattr(view, 'get_querystringfilter_form'):
            return view.get_querystringfilter_form(request, self)

        Form = self.get_form_class(request, view)
        self._form = Form(request.GET, prefix=self.form_prefix)
        return self._form

    def to_html(self, request, queryset, view):
        template = loader.get_template(self.template)
        context = {'form': self.get_form(request, view),
                   'header': 'aaaaaa'}
        return template.render(context, request)

    @lru_cache(100)
    def get_schema_fields(self, view):
        model = view.serializer_class.Meta.model
        self.opts = model._meta

        ret = []
        for field in view.filter_fields:
            try:
                model_field = model._meta.get_field(field)
                description = model_field.help_text
                coreapi_type = SCHEMAMAP.get(type(model_field), coreschema.String)
            except FieldDoesNotExist:
                description = ""
                coreapi_type = coreschema.String
            ret.append(coreapi.Field(
                name=field,
                required=False,
                location='query',
                schema=coreapi_type(
                    title=force_text(field),
                    description=description

                ),
                description='--',
                example='example'))
        return ret

    def field_type(self, field_name):
        try:
            field_object = self.opts.get_field(field_name)
            if isinstance(field_object, BooleanField):
                return bool
        except FieldDoesNotExist:
            return self.field_casting.get(field_name, str)

    @property
    def query_params(self):
        """
        More semantically correct name for request.GET.
        """
        return self.request._request.GET

    @property
    def excluded_query_params(self):
        params_list = [api_settings.URL_FORMAT_OVERRIDE]
        return params_list

    def ignore_filter(self, request, field, view):
        if hasattr(view, 'drf_ignore_filter'):
            return view.drf_ignore_filter(request, field)
        return False

    def _get_mapping(self, view):
        if hasattr(view, 'get_serializer'):
            # try:
            return view.get_serializer().fields
        else:
            # except AttributeError:
            return {}

    def _get_filters(self, request, queryset, view):  # noqa
        """
        filter queryset based on http querystring arguments

        Accepted synthax:

        - exclude null values: country__not=><
        - only values in list: &country__id__in=176,20
        - exclude values in list: &country__id=176,20

        """
        self.opts = queryset.model._meta
        filter_fields = getattr(view, 'filter_fields', None)
        self.exclude = {}
        self.filters = {}

        if filter_fields:
            blacklist = RexList(getattr(view, 'filter_blacklist', []))
            mapping = self._get_mapping(view)

            for fieldname_arg in self.query_params:
                raw_value = self.query_params.get(fieldname_arg)
                if raw_value in ["''", '""']:
                    raw_value = ""

                negate = fieldname_arg[-1] == "!"

                if negate:
                    filter_field_name = fieldname_arg[:-1]
                    TARGET = self.exclude
                else:
                    TARGET = self.filters
                    filter_field_name = fieldname_arg

                if filter_field_name in self.excluded_query_params:
                    continue
                if self.ignore_filter(request, filter_field_name, view):
                    continue
                try:
                    if filter_field_name in blacklist:
                        raise InvalidQueryArgumentError(fieldname_arg)
                    parts = None
                    if '__' in filter_field_name:
                        parts = filter_field_name.split('__')
                        filter_field_name = parts[0]
                        op = parts[-1]
                    else:
                        op = ''
                    processor = getattr(self, 'process_{}'.format(filter_field_name),
                                        getattr(view, 'drfqs_filter_{}'.format(filter_field_name), None))

                    if (filter_field_name not in filter_fields) and (not processor):
                        self.unknown_arguments.append((fieldname_arg, filter_field_name))
                        continue
                        # raise InvalidQueryArgumentError(filter_field_name)
                    if raw_value is None and not processor:
                        continue
                    # field is configured in Serializer
                    # so we use 'source' attribute
                    if filter_field_name in mapping:
                        real_field_name = mapping[filter_field_name].source
                        # if '.' in real_field_name:
                        #     real_field_name = real_field_name.split('.')[0]
                        # field_name = real_field_name.replace('.', '__')
                    else:
                        real_field_name = filter_field_name

                    if processor:
                        payload = {'field': filter_field_name,
                                   'request': request,
                                   'param': fieldname_arg,
                                   'negate': negate,
                                   'op': op,
                                   'field_name': real_field_name,
                                   'parts': parts,
                                   'value': raw_value,
                                   'real_field_name': real_field_name}
                        _f, _e = processor(dict(self.filters), dict(self.exclude), **payload)
                        self.filters.update(**_f)
                        self.exclude.update(**_e)
                    else:
                        if not raw_value:
                            continue
                        # field_object = opts.get_field(real_field_name)
                        value_type = self.field_type(real_field_name)
                        if parts:
                            f = "{}__{}".format(real_field_name, "__".join(parts[1:]))
                        else:
                            f = filter_field_name
                        if op in ['in', 'contained_by']:
                            value = raw_value.split(',')
                        elif op == 'acontains':
                            value = raw_value.split(',')
                            f = f.replace('__acontains', '__contains')
                        elif op == 'isnull':
                            value = parse_bool(raw_value)
                        elif value_type == bool:
                            value = parse_bool(raw_value)
                        else:
                            value = raw_value
                        TARGET[f] = value
                except ValueError:
                    raise InvalidQueryValueError(fieldname_arg, raw_value)
                except QueryFilterException:
                    raise
                except Exception as e:
                    logger.exception(e)
                    raise
        return self.filters, self.exclude

    def filter_queryset(self, request, queryset, view):
        self.request = request
        try:
            filters, exclude = self._get_filters(request, queryset, view)
            request.api_info['qs_filter'] = filters
            request.api_info['qs_exclude'] = exclude
            qs = queryset.filter(**filters).exclude(**exclude)
            logger.debug("""Filtering using:
{}
{}""".format(filters, exclude))
            # if '_distinct' in self.query_params:
            #     f = self.get_param_value('_distinct')
            #     qs = qs.order_by(*f).distinct(*f)
            return qs
        except FieldError as e:
            raise QueryFilterException(str(e))
        except (InvalidFilterError, QueryFilterException) as e:
            logger.exception(e)
            raise
        # except Exception as e:
        #     logger.exception(e)
        #     raise FilteringError(e)
