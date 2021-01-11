import os
from urllib.parse import parse_qsl, urlencode, urlparse

from rest_framework.settings import api_settings


def get_viewset(obj):
    if hasattr(obj, '__name__'):
        name = obj.__name__
    elif hasattr(obj, '__class__') and hasattr(obj.__class__, '__name__'):
        name = obj.__class__.__name__
    else:
        name = '<unknown>'

    if hasattr(obj, '__module__'):
        module = obj.__module__
        name = '%s.%s' % (module, name)

    return name


def get_ident(request):
    """
    Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
    if present and number of proxies is > 0. If not use all of
    HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
    """
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = request.META.get('REMOTE_ADDR')
    num_proxies = api_settings.NUM_PROXIES

    if num_proxies is not None:
        if num_proxies == 0 or xff is None:
            return remote_addr
        addrs = xff.split(',')
        client_addr = addrs[-min(num_proxies, len(addrs))]
        return client_addr.strip()

    return ''.join(xff.split()) if xff else remote_addr


def humanize_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)


def get_hostname():
    return os.environ.get('HOSTNAME')


def get_query_string(params, new_params=None, remove=None):
    if new_params is None:
        new_params = {}
    if remove is None:
        remove = []
    p = params.copy()
    for r in remove:
        for k in list(p):
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    return '?%s' % urlencode(sorted(p.items()))


def parse_url(url, remove=None):
    if remove is None:
        remove = []
    parts = urlparse(url)
    params = dict(parse_qsl(parts.query))
    return parts.path, {k: v for k, v in params.items() if k not in remove}
