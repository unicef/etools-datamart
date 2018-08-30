# -*- coding: utf-8 -*-

import logging
import time

from django.contrib import messages
from django.core.cache import caches
from rest_framework.throttling import BaseThrottle
from unicef_rest_framework.config import conf
from unicef_rest_framework.models import UserAccessControl

logger = logging.getLogger(__name__)


class APIRateThrottle(BaseThrottle):
    cache = caches['default']
    timer = time.time
    cache_format = 'throttle_%(scope)s_%(ident)s'
    rate = None

    def __init__(self):
        self.num_requests = 0
        self.key = None

    def get_rate(self, request, view):
        return self.rate

    def get_cache_key(self, request, view):
        raise NotImplementedError

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        return (num_requests, duration)

    def _add_throttle_info(self, request):
        req = conf.get_current_request()
        req._throttling_rate = self.rate
        req._throttling_remaining = self.num_requests - len(self.history)
        req._throttling_reset = int(self.wait())

    def allow_request(self, request, view):
        try:
            self.rate = self.get_rate(request, view)
            if self.rate is None:
                return True
            self.key = self.get_cache_key(request, view)

            if self.key is None:
                return True
            self.num_requests, self.duration = self.parse_rate(self.rate)

            self.history = self.cache.get(self.key, [])
            self.now = self.timer()
            # Drop any requests from the history which have now passed the
            # throttle duration
            while self.history and self.history[-1] <= self.now - self.duration:
                self.history.pop()

            if len(self.history) >= self.num_requests:
                allow = self.throttle_failure()
            else:
                allow = self.throttle_success()
            self._add_throttle_info(request)
            return allow
        except Exception:
            logger.critical("Unable to throttle", extra={'request': request,
                                                         'stack': True})
            return True

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        return False

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.history:
            remaining_duration = self.duration - (self.now - self.history[-1])
        else:
            remaining_duration = self.duration

        available_requests = self.num_requests - len(self.history) + 1
        if available_requests <= 0:
            return None

        return remaining_duration / float(available_requests)


class ViewRateThrottle(APIRateThrottle):
    cache_format = 'throttle_%(view)s_%(ident)s'

    def get_rate(self, request, view):
        return getattr(view, 'throttle_rate', None)

    def get_cache_key(self, request, view):
        self.pk = request.user.pk
        ident = self.pk

        return self.cache_format % {
            'view': view.fqn,
            'ident': ident
        }


class ACLRateThrottle(APIRateThrottle):
    cache_format = 'throttle_acl_%(view)s_%(ident)s'
    cache = caches['default']

    def get_rate(self, request, view):
        try:
            service = view.get_service()
        except AttributeError:
            return None
        if request.user.is_superuser:
            return None
        acl = UserAccessControl.objects.filter(user=request.user, service=service).first()

        if acl is None or acl.rate == '*':
            return None

        return acl.rate

    def get_cache_key(self, request, view):
        messages.info(request._request, request._request.user.pk)
        ident = request._request.user.pk

        return self.cache_format % {
            'view': view.fqn,
            'ident': ident
        }
