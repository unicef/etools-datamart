# from celery.utils.log import get_task_logger
#
# from etools_datamart.celery import app
#
# from .models import APIRequestLog
#
# task_logger = get_task_logger(__name__)
#
#
# import logging
# from datetime import datetime, timedelta
#
# from django.contrib.auth import get_user_model
# from django.db.models import Avg, Count, Max, Min, Q, Sum
# from django.db.transaction import atomic
# from django.utils import timezone
#
# from etools_datamart.apps.tracking.models import APIRequestLog
#
# from .counters import DailyCounter, MonthlyCounter, PathCounter, UserCounter
#
# logger = logging.getLogger(__name__)
#
#
# @atomic()
# def aggregate_log():
#     if not APIRequestLog.objects.exists():
#         return 0
#
#     today = timezone.now().date()
#     last = DailyCounter.objects.first()
#     if not last:  # first time
#         current = APIRequestLog.objects.earliest().requested_at.date()
#     else:
#         current = last.day
#
#     last_month = MonthlyCounter.objects.first()
#     if last_month:
#         last_month = MonthlyCounter.objects.first().day.month
#     else:
#         last_month = None
#
#     processed = 0
#     while current < today:
#         qs = APIRequestLog.objects.filter(requested_at__day=current.day,
#                                           requested_at__month=current.month,
#                                           requested_at__year=current.year)
#         found = qs.exists()
#         if found:
#             qs1 = qs.aggregate(total=Count('id'),
#                                max=Max('response_ms'),
#                                min=Min('response_ms'),
#                                avg=Avg('response_ms'))
#
#             hosts = qs.values_list('remote_addr', flat=True).distinct()
#
#             data = {'response_max': qs1['max'],
#                     'response_min': qs1['min'],
#                     'total': qs1['total'],
#                     'cached': qs.filter(cached=True).count(),
#                     'user': qs.filter(user__isnull=False).count(),
#                     'response_average': qs1['avg'],
#                     'unique_ips': len(hosts),
#                     }
#
#             DailyCounter.objects.update_or_create(day=current, defaults=data)
#
#         _aggregate_path(qs, current)
#         _aggregate_user(qs, current)
#         current = current + timedelta(days=1)
#         if found:
#             # process monthly stats if month is changed
#             if last_month and current.month >= last_month:
#                 prev = current + timedelta(days=-1)
#                 _aggregate_monthly(qs, prev)
#                 last_month = MonthlyCounter.objects.first().day.month
#
#         processed += 1
#
#     # Keep only last 90 days of logs
#     target_limit = today - timedelta(days=90)
#     deleted_logs = APIRequestLog.objects.filter(requested_at__date__lt=target_limit).delete()
#
#     return processed, deleted_logs
#
#
# def _aggregate_path(qs, current):
#     paths = qs.values('path').annotate(total=Count('id'),
#                                        cached=Count('id', only=Q(cached=True)),
#                                        service=Max('service'),
#                                        m1=Max('response_ms'),
#                                        m2=Min('response_ms'))
#     for entry in paths:
#         data = {'total': entry['total'],
#                 'response_max': entry['m1'],
#                 'response_min': entry['m2'],
#                 'cached': entry['cached'],
#                 }
#         PathCounter.objects.update_or_create(day=current,
#                                              service_id=entry['service'],
#                                              path=entry['path'],
#                                              defaults=data)
#
#
# def _aggregate_user(qs, current):
#     users = qs.values('user').annotate(total=Count('id'),
#                                        cached=Count('id', only=Q(cached=True)),
#                                        m1=Max('response_ms'),
#                                        m2=Min('response_ms'))
#     for entry in users:
#         if entry['user']:
#             data = {'total': entry['total'],
#                     'response_max': entry['m1'],
#                     'response_min': entry['m2'],
#                     'cached': entry['cached'],
#                     }
#             UserCounter.objects.update_or_create(day=current,
#                                                  user=get_user_model().objects.get(pk=entry['user']),
#                                                  defaults=data)
#
#
# def _aggregate_monthly(qs, first_day_of_month):
#     qsx = DailyCounter.objects.filter(day__month=first_day_of_month.month,
#                                       day__year=first_day_of_month.year)
#     qsm = qsx.aggregate(total=Sum('total'),
#                         cached=Sum('cached'),
#                         users=Sum('user'),
#                         max=Max('response_max'),
#                         min=Min('response_min'))
#
#     hosts = qs.values_list('remote_addr', flat=True).distinct()
#     avg = (qsm['max'] - qsm['min']) / float(qsm['total'])
#
#     data = {'response_max': qsm['max'],
#             'response_min': qsm['min'],
#             'total': qsm['total'],
#             'cached': qsm['cached'],
#             'user': qsm['users'],
#             'response_average': avg,
#             'unique_ips': len(hosts),
#             }
#     MonthlyCounter.objects.update_or_create(day=datetime(first_day_of_month.year,
#                                                          first_day_of_month.month,
#                                                          1),
#                                             defaults=data)
#
# @app.task
# def task_aggregate_log():
#     task_logger.info('Starting logs aggregation')
#     return APIRequestLog.objects.aggregate()
