# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler
from strategy_field.utils import get_attr


class ApiException(APIException):
    def __init__(self, *args, **kwargs):
        self._data = kwargs.pop('data', None)
        self._cause = kwargs.pop('cause', None)
        self._tb = kwargs.pop('tb', None)

        super(ApiException, self).__init__(*args, **kwargs)


class TokenExpired(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token expired')


class TokenDecodeError(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token tampered with')


class InvalidQueryArgumentError(ApiException):
    def __init__(self, field, *args, **kwargs):
        self.field = field
        super(InvalidQueryArgumentError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Invalid parameter '{}'".format(self.field)


class InvalidQueryValueError(ApiException):

    def __init__(self, field, value, hint=None, *args, **kwargs):
        self.field = field
        self.value = value
        self.hint = hint
        super(InvalidQueryValueError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Invalid value '{}' for parameter {}".format(self.value, self.field)


class InvalidSerializerError(InvalidQueryValueError):
    argument = 'serializer'


class InvalidFilterError(ApiException):
    def __init__(self, field, *args, **kwargs):
        self.field = field
        super(InvalidFilterError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Invalid filter '{}'".format(self.field)


class FilteringError(ApiException):
    def __init__(self, reason, *args, **kwargs):
        self.reason = reason
        super(FilteringError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Invalid query: '{}'".format(self.reason)


def handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response = Response({}, status=401)
        response.data['detail'] = str(exc)
        response.data['error'] = str(exc)
    elif isinstance(exc, ApiException):
        if get_attr(exc, 'reason.messages'):
            err = ",".join(map(str, (exc.reason.messages)))
        else:
            err = str(exc)
        response = Response({'error': err}, status=400)
    elif isinstance(exc, ValidationError):
        if response is None:
            response = Response({}, status=400)
        if 'error_dics' in exc and 'non_field_errors' in exc.error_dict:
            response.data['error'] = ",".join(map(str, exc.error_dict['non_field_errors']))
        else:
            response.data['error'] = str(exc)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
