import logging

from django.conf import settings
from django.db import connections, models
from django.utils.timezone import now

from strategy_field.fields import StrategyClassField

logger = logging.getLogger(__name__)


class APIRequestLogManager(models.Manager):
    def truncate(self):
        conn = connections["default"]
        cursor = conn.cursor()
        cursor.execute(f'TRUNCATE TABLE "{self.model._meta.db_table}"')


class APIRequestLog(models.Model):
    """Logs API requests by time, user, etc"""

    # user or None for anon
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, blank=True, null=True)

    # timestamp of request
    requested_at = models.DateTimeField(db_index=True, default=now)

    # number of milliseconds to respond
    response_ms = models.PositiveIntegerField("ms", default=0)
    response_length = models.BigIntegerField("length", default=0)

    # request path
    path = models.CharField(max_length=255, db_index=True)

    # remote IP address of request
    remote_addr = models.GenericIPAddressField(blank=True, null=True)

    # originating host of request
    host = models.URLField()

    # HTTP method (GET, etc)
    method = models.CharField(max_length=10)

    # query params
    query_params = models.TextField()

    # POST body data
    data = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=255)
    cached = models.BooleanField(default=False)

    # extra
    service = models.CharField(max_length=100, blank=True, null=True)
    viewset = StrategyClassField(blank=True, null=True)

    class Meta:
        verbose_name = "Access Log"
        verbose_name_plural = "Access Log"
        ordering = ("-id",)
        get_latest_by = "requested_at"

    objects = APIRequestLogManager()

    def __str__(self):
        return f"Request: {self.requested_at} {self.path}"
