import logging
from functools import lru_cache

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import FieldError, ValidationError
from django.db import models

from strategy_field.utils import fqn

from .application import Application
from .service import Service

logger = logging.getLogger(__name__)


class InvalidRule(ValidationError):
    pass


class InvalidField(InvalidRule):
    pass


class InvalidValue(InvalidRule):
    pass


class InvalidOperator(InvalidRule):
    pass


class SystemFilterHandler(object):
    def __init__(self, filter):
        self.filter = filter
        super().__init__()

    def filter_queryset(self, queryset):
        return queryset


class SystemFilterManager(models.Manager):
    @lru_cache()
    def match(self, request, view):
        if request.user and request.user.is_authenticated:
            try:
                return SystemFilter.objects.get(service=view.get_service(),
                                                user=request.user)
            except SystemFilter.DoesNotExist:
                return None


class SystemFilter(models.Model):
    """ Store 'hardcoded' filters per user
    @see AutoFilterRule
    """
    application = models.ForeignKey(Application, models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, models.CASCADE)
    description = models.TextField(blank=True)
    handler = models.CharField(max_length=500, default=fqn(SystemFilterHandler))

    objects = SystemFilterManager()

    class Meta:
        unique_together = (('service', 'user'),
                           ('service', 'group'))

    def __str__(self):
        return f"{self.user}/{self.service}"

    def set_rule(self, **kwargs):
        for field, value in kwargs.items():
            self.test(**{field: value})

            r, __ = self.rules.get_or_create(field=field)
            r.value = value
            r.save()

    def test(self, **kwargs):
        try:
            self.service.viewset().get_queryset().filter(**kwargs)
        except (FieldError, TypeError) as e:
            raise InvalidField(e)

    @lru_cache()
    def get_filters(self):
        f = {}
        for r in self.rules.all():
            f[r.field] = r.value
        return f

    @lru_cache()
    def get_querystring(self):
        f = []
        for field, value in self.get_filters().items():
            f.append("{0}={1}".format(field, value))
        return "&".join(f)

    def filter_queryset(self, queryset):
        return queryset.filter(**self.get_filters())


class SystemFilterFieldRule(models.Model):
    filter = models.ForeignKey(SystemFilter, models.CASCADE, related_name='rules')
    field = models.CharField(max_length=500)
    value = models.CharField(max_length=300, blank=True, null=True)
    override_field = models.BooleanField(default=False)

    class Meta:
        unique_together = ('filter', 'field')

    def __str__(self):
        return f"{self.filter}: {self.field}={self.value}"


class SystemFilterParam(models.Model):
    filter = models.ForeignKey(SystemFilter, models.CASCADE)
    param = models.CharField(max_length=300)
    value = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        unique_together = ('filter', 'param')
