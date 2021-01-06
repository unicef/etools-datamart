import json
import logging

from django.conf import settings
from django.db.models import F
from django.utils.timezone import now

from strategy_field.utils import fqn

from etools_datamart.apps.tracking import config

from .models import APIRequestLog, DailyCounter, MonthlyCounter, PathCounter, UserCounter

# from unicef_rest_framework.state import state


logger = logging.getLogger(__name__)


def log_request(**kwargs):
    log = APIRequestLog.objects.create(**kwargs)

    if settings.ENABLE_LIVE_STATS:
        # lastMonth = (log.requested_at.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        lastMonth = log.requested_at.replace(day=1)

        def _update_stats(target, **extra):

            extra['total'] = F('total') + 1
            extra['response_max'] = max(target.response_max, log.response_ms)
            extra['response_min'] = min(target.response_min, log.response_ms)
            extra['response_avg'] = target.response_max / target.total
            extra['cached'] = F('cached') + int(log.cached)
            for k, v in extra.items():
                setattr(target, k, v)
            try:
                target.save()
            except Exception as e:  # pragma: no cover
                logger.error(f"""Error updating {target.__class__.__name__}: {e}
{extra}
""")

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
        defaults['users'] = 1
        daylog, isnew = DailyCounter.objects.get_or_create(day=log.requested_at,
                                                           defaults=defaults)
        if not isnew:
            _update_stats(daylog,
                          users=UserCounter.objects.filter(day=log.requested_at).count())


def record_to_kwargs(request, response):
    user = None
    api_info = getattr(request, 'api_info')
    if request.user and request.user.is_authenticated:
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
    view = api_info.get('view', None)
    if not view:  # pragma: no cover
        return None
    viewset = fqn(view)
    service = api_info.get("service")
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
                service=service.name,
                cached=request.api_info.get('cache-hit', False),  # see api.common.APICacheResponse
                content_type=media_type)


#
# class AsyncLogger(AsyncQueue):
#     def _process(self, record):
#         values = record_to_kwargs(**record)
#         if values:
#             log_request(**values)


class StatsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def log(self, request, response):
        try:
            values = record_to_kwargs(request, response)
            if values:
                log_request(**values)
        except Exception as e:  # pragma: no cover
            logger.exception(e)

    def __call__(self, request):

        request.timestamp = now()

        response = self.get_response(request)
        if response.status_code == 200 and \
                hasattr(request, 'api_info') and \
                config.TRACK_PATH.match(request.path) and \
                not hasattr(request, '_is_preload_internal_request'):
            self.log(request, response)
        return response

#
# class ThreadedStatsMiddleware(StatsMiddleware):
#     def __init__(self, get_response):
#         super().__init__(get_response)
#         self.worker = AsyncLogger()
#
#     def log(self, request, response):
#         self.worker.queue({'request': request, 'response': response})
