# -*- coding: utf-8 -*-

import logging

from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.functional import cached_property
from strategy_field.fields import StrategyClassField
from unicef_rest_framework.config import conf

from .. import acl
from .base import MasterDataModel

logger = logging.getLogger(__name__)

cluster_cache = caches[conf.API_CACHE]


class Service(MasterDataModel):
    name = models.CharField(max_length=100, help_text='unique service name',
                            db_index=True, unique=True)
    description = models.TextField(blank=True, null=True)
    viewset = StrategyClassField(help_text='class FQN',
                                 unique=True, db_index=True)
    access = models.IntegerField(choices=[(k, v) for k, v in acl.ACL_LABELS.items()],
                                 default=acl.ACL_ACCESS_LOGIN,
                                 help_text="Required privileges")

    confidentiality = models.IntegerField(choices=acl.CONFIDENTIALITY_CHOICES,
                                          default=acl.CLASS_INTERNAL)

    hidden = models.BooleanField(default=False)

    cache_version = models.IntegerField(default=1)
    cache_ttl = models.CharField(default='1d', max_length=5)
    # cache_expire = models.TimeField(blank=True, null=True)
    cache_key = models.CharField(max_length=1000,
                                 null=True, blank=True,
                                 help_text='Key used to invalidate service cache')

    linked_models = models.ManyToManyField(ContentType,
                                           blank=True,
                                           help_text="models that the service depends on")

    class Meta:
        ordering = ('name',)
        permissions = (("do_not_scramble", "Can read any service unscrambled"),)

    def invalidate_cache(self):
        Service.objects.filter(id=self.pk).update(cache_version=F("cache_version") + 1)
        self.refresh_from_db()
        cluster_cache.set('{}{}'.format(self.pk, self.name), True)

    def cache_is_invalid(self):
        return cluster_cache.get('{}{}'.format(self.pk, self.name), True)

    def get_access_level(self):
        # administrators cannot go lower than coded value
        return max(self.access, self.viewset.default_acl)

    @cached_property
    def entry_point(self):
        try:
            for __, viewset, base_name, __ in conf.router.registry:
                if viewset == self.viewset:
                    return reverse('{}-list'.format(base_name))
        except Exception as e:
            logger.exception(e)
            return None

    @cached_property
    def display_name(self):
        return "{} ({})".format(self.viewset.__name__, self.viewset.source)

    @cached_property
    def managed_model(self):
        try:
            v = self.viewset()
            m = v.get_queryset().model
            del v
            return m
        except TypeError:
            return None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            try:
                self.viewset._service = None
            except Exception as e:
                logger.exception(e)
        super(Service, self).save(force_insert, force_update, using, update_fields)
        # self.invalidate_cache()

    def __str__(self):
        return self.name
        # return "Service:{} ({})".format(self.name, self.viewset)


class CacheVersion(Service):
    class Meta:
        proxy = True
