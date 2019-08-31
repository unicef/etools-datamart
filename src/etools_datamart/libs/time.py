from datetime import datetime

from django.conf import settings
from django.utils import timezone


def strfelapsed(seconds):
    # seconds = 9.888888888888886 * 60 * 60
    if seconds:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
    else:
        hours = minutes = seconds = 0
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def make_aware(value):
    """Make the given datetime aware of a timezone."""
    if settings.USE_TZ:
        # naive datetimes are assumed to be in UTC.
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.utc)
        # then convert to the Django configured timezone.
        default_tz = timezone.get_default_timezone()
        value = timezone.localtime(value, default_tz)
    return value


def fromtimestamp(value):
    """Return an aware or naive datetime from the given timestamp."""
    if settings.USE_TZ:
        return make_aware(datetime.utcfromtimestamp(value))
    else:
        return datetime.fromtimestamp(value)


def correct_awareness(value):
    """Fix the given datetime timezone awareness."""
    if isinstance(value, datetime):
        if settings.USE_TZ:
            return make_aware(value)
        elif timezone.is_aware(value):
            default_tz = timezone.get_default_timezone()
            return timezone.make_naive(value, default_tz)
    return value
