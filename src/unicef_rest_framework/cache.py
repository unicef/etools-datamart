import re

from django.core.cache import caches
from django.utils.translation import ugettext as _
from humanize.i18n import ngettext
from humanize.time import date_and_delta

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

#
# def method_cache(ttl=0, cache_key=None):
#     """
#     A `seconds` value of `0` means that we will not memcache it.
#
#     If a result is cached on instance, return that first.  If that fails, check
#     memcached. If all else fails, hit the db and cache on instance and in memcache.
#
#     ** NOTES:
#     1) Methods that return None are always "recached".
#     2) `instance` can either instance or class (if applied to a @classmethod)
#     """
#     seconds = parse_ttl(ttl)
#
#     def inner_cache(method):
#
#         def x(instance, *args, **kwargs):
#             key = cache_key or sha224("".join((str(id(instance)),
#                                               str(method.__name__),
#                                               str(args),
#                                               str(kwargs)).hexdigest()))
#             if hasattr(instance, key):
#                 # has on class cache, return that
#                 result = getattr(instance, key)
#             else:
#                 result = cache.get(key)
#
#                 if result is None:
#                     # all caches failed, call the actual method
#                     result = method(instance, *args, **kwargs)
#
#                     # save to memcache and class attr
#                 if seconds and isinstance(seconds, int):
#                     cache.set(key, result, seconds)
#                 setattr(instance, key, result)
#             return result
#
#         return x
#
#     return inner_cache
#
#
# def func_cache(ttl):
#     """
#     A `seconds` value of `0` means that we will not memcache it.
#
#     If a result is cached on instance, return that first.  If that fails, check
#     memcached. If all else fails, hit the db and cache on instance and in memcache.
#
#     ** NOTE: Methods that return None are always "recached".
#     """
#     seconds = parse_ttl(ttl)
#
#     def inner_cache(method):
#         @wraps(method)
#         def x(*args, **kwargs):
#             key = sha224(str(method.__module__) + str(method.__name__) + str(args) + str(kwargs)).hexdigest()
#             result = cache.get(key)
#             if result is None:
#                 # all caches failed, call the actual method
#                 result = method(*args, **kwargs)
#
#                 # save to memcache and class attr
#                 if seconds and isinstance(seconds, int):
#                     cache.set(key, result, seconds)
#             return result
#
#         return x
#
#     return inner_cache
#
#
# def inline_cache(callable, seconds=0, key=None, *args, **kwargs):  # pragma: no cover
#     key = key or sha224(str(callable.__module__) + str(callable.__name__) + str(args) + str(kwargs)).hexdigest()
#
#     def x(*args, **kwargs):
#         result = cache.get(key)
#         if result is None:
#             # all caches failed, call the actual method
#             result = callable(*args, **kwargs)
#
#             # save to memcache and class attr
#             if seconds and isinstance(seconds, int):
#                 cache.set(key, result, seconds)
#         return result
#
#     return x
#

# backport of Python's 3.3 lru_cache, written by Raymond Hettinger and
# licensed under MIT license, from:
# <http://code.activestate.com/recipes/578078-py26-and-py30-backport-of-python-33s-lru-cache/>
# Should be removed when Django only supports Python 3.2 and above.

#
# _CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])
#
#
# class _HashedSeq(list):
#     __slots__ = 'hashvalue'
#
#     def __init__(self, tup, hash=hash):
#         self[:] = tup
#         self.hashvalue = hash(tup)
#
#     def __hash__(self):
#         return self.hashvalue
#
#
# def _make_key(args, kwds, typed,
#               kwd_mark=(object(),),
#               fasttypes={int, str, frozenset, type(None)},
#               sorted=sorted, tuple=tuple, type=type, len=len):
#     'Make a cache key from optionally typed positional and keyword arguments'
#     key = args
#     if kwds:
#         sorted_items = sorted(kwds.items())
#         key += kwd_mark
#         for item in sorted_items:
#             key += item
#     if typed:
#         key += tuple(type(v) for v in args)
#         if kwds:
#             key += tuple(type(v) for k, v in sorted_items)
#     elif len(key) == 1 and type(key[0]) in fasttypes:
#         return key[0]
#     return _HashedSeq(key)
