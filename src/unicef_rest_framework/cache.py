import re
import time

from django.core.cache import caches
from django.utils.http import quote_etag
from django.utils.translation import ugettext as _

from constance import config
from humanize.i18n import ngettext
from humanize.time import date_and_delta
from rest_framework_extensions.cache.decorators import CacheResponse
from rest_framework_extensions.etag.decorators import ETAGProcessor
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.bits import KeyBitBase, QueryParamsKeyBit
from rest_framework_extensions.key_constructor.constructors import KeyConstructor
from rest_framework_extensions.settings import extensions_api_settings
from strategy_field.utils import fqn

from unicef_rest_framework.models import SystemFilter

cache = caches['default']


def parse_ttl(ttl):
    """
    :param ttl:
    :return:

    >>> parse_ttl('1w')
    604800

    """
    durations = {'s': 1,
                 'm': 60,  # minute
                 'h': 3600,  # hour
                 'd': 86400,  # day
                 'w': 604800,  # week
                 'y': 31536000}  # year
    rex = re.compile(r'((\d+)([smhdwy]))')
    try:
        groups = rex.findall(ttl)
        if not groups:
            return int(ttl)
        return sum([int(g[1]) * durations[g[2]] for g in groups])
    except TypeError:
        return int(ttl)


def humanize_ttl(value, months=True):  # noqa
    """Given a timedelta or a number of seconds, return a natural
    representation of the amount of time elapsed.  This is similar to
    ``naturaltime``, but does not add tense to the result.  If ``months``
    is True, then a number of months (based on 30.5 days) will be used
    for fuzziness between years."""
    # now = _now()
    date, delta = date_and_delta(value)
    if date is None:
        return value

    use_months = months

    seconds = abs(delta.seconds)
    days = abs(delta.days)
    years = days // 365
    days = days % 365
    months = int(days // 30.5)

    if not years and days < 1:
        if seconds == 0:
            return _("a moment")
        elif seconds == 1:
            return _("1 second")
        elif seconds < 60:
            return ngettext("%d second", "%d seconds", seconds) % seconds
        elif 60 <= seconds < 120:
            return _("1 minute")
        elif 120 <= seconds < 3600:
            minutes = seconds // 60
            return ngettext("%d minute", "%d minutes", minutes) % minutes
        elif 3600 <= seconds < 3600 * 2:
            return _("1 hour")
        elif 3600 < seconds:
            hours = seconds // 3600
            return ngettext("%d hour", "%d hours", hours) % hours
    elif years == 0:
        if days == 1:
            return _("1 day")
        if not use_months:
            return ngettext("%d day", "%d days", days) % days
        else:
            if not months:
                return ngettext("%d day", "%d days", days) % days
            elif months == 1:
                return _("a month")
            else:
                return ngettext("%d month", "%d months", months) % months
    elif years == 1:
        if not months and not days:
            return _("a year")
        elif not months:
            return ngettext("1 year, %d day", "1 year, %d days", days) % days
        elif use_months:
            if months == 1:
                return _("1 year, 1 month")
            else:
                return ngettext("1 year, %d month",
                                "1 year, %d months", months) % months
        else:
            return ngettext("1 year, %d day", "1 year, %d days", days) % days
    else:
        return ngettext("%d year", "%d years", years) % years


class CacheVersionKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        version = view_instance.get_service().cache_version
        view_instance.request._request.api_info['cache-version'] = version
        return {'cache_version': str(version),
                'version': str(config.CACHE_VERSION)}


class SystemFilterKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        flt = SystemFilter.objects.match(request, view_instance)
        request._request._system_filters = flt
        qs = flt.get_querystring() if flt else ''
        request._request.api_info['system-filters'] = qs
        return {'systemfilter': qs}


class QueryPathKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        return {'path': str(request.path)}


class SuperuserKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        return {'admin': request.user.is_superuser}


class IsStaffKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        return {'staff': request.user.is_staff}


class DevelopKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        if not config.CACHE_ENABLED:
            return {'dev': str(time.time())}
        if request.META.get('HTTP_X_DM_CACHE') == 'disabled':
            return {'dev': str(time.time())}
        return {}


class SmartQueryParamsKeyBit(QueryParamsKeyBit):
    """
    Return example:
        {'part': 'Londo', 'callback': 'jquery_callback'}

    """

    def get_source_dict(self, params, view_instance, view_method, request, args, kwargs):
        values = request.GET.copy()
        if not values.get('ordering', None) == view_instance.ordering:
            values['ordering'] = view_instance.ordering
        if not values.get(view_instance.serializer_field_param, None):
            values[view_instance.serializer_field_param] = 'std'
        return values


class ListKeyConstructor(KeyConstructor):
    cache_version = CacheVersionKeyBit()
    system_filter = SystemFilterKeyBit()
    path = QueryPathKeyBit()
    unique_method_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    headers = bits.HeadersKeyBit(['Accept'])
    dev = DevelopKeyBit()
    admin = SuperuserKeyBit()
    staff = IsStaffKeyBit()
    querystring = SmartQueryParamsKeyBit()

    def get_key(self, view_instance, view_method, request, args, kwargs):
        key = super().get_key(view_instance, view_method, request, args, kwargs)
        view_instance.request._request.api_info['cache-key'] = key
        return key


class APIETAGProcessor(ETAGProcessor):
    def is_if_none_match_failed(self, res_etag, etags, if_none_match):
        if res_etag and if_none_match:
            return quote_etag(res_etag) in etags or '*' in etags
        else:
            return False


class APICacheResponse(CacheResponse):
    def __init__(self,
                 timeout=None,
                 key_func=None,
                 cache=None,
                 cache_errors=None):
        self.cache_name = cache or extensions_api_settings.DEFAULT_USE_CACHE
        super(APICacheResponse, self).__init__(timeout=timeout, key_func=key_func,
                                               cache=cache, cache_errors=cache_errors)

    def process_cache_response(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        cache = caches[self.cache_name]
        if config.CACHE_ENABLED:
            key = self.calculate_key(
                view_instance=view_instance,
                view_method=view_method,
                request=request,
                args=args,
                kwargs=kwargs
            )
            response = cache.get(key)
        else:
            response = None
            key = '--'
        if not response:
            view_instance.request._request.api_info['cache-hit'] = False
            response = view_method(view_instance, request, *args, **kwargs)
            response = view_instance.finalize_response(request, response, *args, **kwargs)
            response.render()  # should be rendered, before picklining while storing to cache
            if config.CACHE_ENABLED and response.status_code == 200:  # pragma: no cover
                expire = parse_ttl(view_instance.get_service().cache_ttl or '1y')
                cache.set(key, response, expire)
        else:
            view_instance.request._request.api_info['cache-hit'] = True

        view_instance.store('cache-ttl', view_instance.get_service().cache_ttl)
        view_instance.store('service', view_instance.get_service())
        view_instance.store('view', fqn(view_instance))
        if not hasattr(response, '_closable_objects'):  # pragma: no cover
            response._closable_objects = []

        return response


etag = APIETAGProcessor
cache_response = APICacheResponse


def get_key(key):
    return f"{key}:{config.CACHE_VERSION}x"
