# -*- coding: utf-8 -*-

import datetime
import json
import logging

from django.conf import settings
from django.db.models import F
from django.utils.timezone import now
from strategy_field.utils import fqn, get_attr

from etools_datamart.state import state

from .asyncqueue import AsyncQueue
from .models import APIRequestLog, DailyCounter, MonthlyCounter, PathCounter, UserCounter

logger = logging.getLogger(__name__)


def log_request(**kwargs):
    log = APIRequestLog.objects.create(**kwargs)
    if settings.ENABLE_LIVE_STATS:  # pragma: no cover
        lastMonth = (log.requested_at.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

        def _update_stats(target, **overrides):
            target.total = F('total') + target.total
            target.response_max = max(target.response_max, log.response_ms)
            target.response_min = min(target.response_min, log.response_ms)
            target.response_avg = target.response_max / target.total
            target.cached = F('cached') + int(log.cached)
            for k, v in overrides.items():
                setattr(target, k, v)

            target.save()

        defaults = {"total": 1,
                    "cached": int(log.cached),
                    "response_max": log.response_ms,
                    "response_min": log.response_ms,
                    "response_average": log.response_ms,
                    }
        # use get_or_create due https://code.djangoproject.com/ticket/25195
        # UserCounter
        userlog, isnew = UserCounter.objects.get_or_create(day=log.requested_at,
                                                           user=log.user,
                                                           defaults=defaults)
        if not isnew:
            _update_stats(userlog)

        # PathCounter
        pathlog, isnew = PathCounter.objects.get_or_create(day=log.requested_at,
                                                           path=log.path,
                                                           defaults=defaults)
        if not isnew:
            _update_stats(pathlog)

        # MonthlyCounter
        monthlog, isnew = MonthlyCounter.objects.get_or_create(day=lastMonth,
                                                               user=log.user,
                                                               defaults=defaults)
        if not isnew:
            _update_stats(monthlog)

        # DailyCounter
        defaults['user'] = 1
        daylog, isnew = DailyCounter.objects.get_or_create(day=log.requested_at,
                                                           defaults=defaults)
        if not isnew:
            _update_stats(daylog,
                          user=UserCounter.objects.filter(day=log.requested_at).count())


def record_to_kwargs(request, response):
    user = None

    if request.user and request.user.is_authenticated:  # pragma: no cover
        user = request.user

    # compute response time
    response_timedelta = now() - request.timestamp
    response_ms = int(response_timedelta.total_seconds() * 1000)
    response_length = len(response.content)

    # get POST data
    try:
        data_dict = request.POST.dict()
    except AttributeError:  # pragma: no cover # if already a dict, can't dictify
        data_dict = request.data

    try:
        media_type = response.accepted_media_type
    except AttributeError:  # pragma: no cover
        media_type = response['Content-Type'].split(';')[0]
    viewset = getattr(request, 'viewset', None)
    if not viewset:  # pragma: no cover
        return {}
    viewset = fqn(viewset)
    service = get_attr(request, "service.name")
    from unicef_rest_framework.utils import get_ident
    return dict(user=user,
                requested_at=request.timestamp,
                response_ms=response_ms,
                response_length=response_length,
                path=request.path,
                remote_addr=get_ident(request),
                host=request.get_host(),
                method=request.method,
                query_params=json.dumps(request.GET.dict()),
                data=data_dict,
                viewset=viewset,
                service=service,
                cached=state.get('cache-hit') or False,  # see api.common.APICacheResponse
                content_type=media_type)


class AsyncLogger(AsyncQueue):
    def _process(self, record):
        log_request(**record_to_kwargs(**record))


class StatsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def log(self, request, response):
        try:
            log_request(**record_to_kwargs(request, response))
        except Exception as e:  # pragma: no cover
            logger.exception(e)

    def __call__(self, request):

        request.timestamp = now()

        response = self.get_response(request)

        if response.status_code == 200:
            self.log(request, response)
        return response


class ThreadedStatsMiddleware(StatsMiddleware):
    def __init__(self, get_response):
        super(ThreadedStatsMiddleware, self).__init__(get_response)
        self.worker = AsyncLogger()

    def log(self, request, response):
        self.worker.queue({'request': request, 'response': response})
