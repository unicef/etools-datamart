from django.core.cache import cache

from .models import APIRequestLog, DailyCounter, MonthlyCounter, PathCounter, UserCounter


def reset_all_counters():
    for m in DailyCounter, UserCounter, MonthlyCounter, PathCounter:
        m.objects.truncate()


def refresh_all_counters():
    cache.delete("tracking-counters")


def get_all_counters():
    numbers = cache.get("tracking-counters")
    if not numbers:
        numbers = {}
        for m in DailyCounter, UserCounter, MonthlyCounter, PathCounter, APIRequestLog:
            numbers[m._meta.verbose_name] = m.objects.count()
        cache.set("tracking-counters", numbers)

    return numbers
