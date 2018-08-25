# -*- coding: utf-8 -*-
import os

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.settings import api_settings
from unicef_rest_framework.config import conf
from unicef_rest_framework.models import Service


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


def refresh_service_table():
    """
        create a row in the Service table for each known service.
    Note: do not update existing entries.

    :param request:
    :param code:
    :return:
    """
    router = conf.ROUTER
    created = deleted = 0
    for prefix, viewset, basename in router.registry:
        name = getattr(viewset, 'label', viewset.__name__)
        try:
            s, isnew = Service.objects.get_or_create(name=name,
                                                     defaults={
                                                         'viewset': viewset,
                                                         'access': getattr(viewset, 'default_access', conf.DEFAULT_ACCESS),
                                                         'description': getattr(viewset, '__doc__', "")})

            if isnew:
                created += 1
        except IntegrityError:
            s = Service.objects.get(name=name)
            # s.source=source
            s.icon = viewset.icon
            s.description = viewset.short_description

        s.viewset = viewset
        s.save()

        # if viewset_fqn in manager:
        #     if not s.cache.refresh_function:
        #         refresh_function, ttl_green, ttl_red = manager[viewset_fqn]
        #         s.cache.refresh_function = fqn(refresh_function)
        #         s.cache.ttl_green = ttl_green
        #         s.cache.ttl_red = ttl_red
        #         s.cache.save()

    for service in Service.objects.all():
        try:
            assert service.viewset
        except ValidationError:
            service.delete()
            deleted += 1

    return created, deleted


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
