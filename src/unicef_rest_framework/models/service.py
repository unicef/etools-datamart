# -*- coding: utf-8 -*-

import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.utils.functional import cached_property

from rest_framework.reverse import reverse
from strategy_field.fields import StrategyClassField

from unicef_rest_framework.config import conf

from .. import acl
from .base import MasterDataModel

logger = logging.getLogger(__name__)


class ServiceManager(models.Manager):
    def invalidate_cache(self, **kwargs):
        Service.objects.filter(**kwargs).update(cache_version=F("cache_version") + 1)
        for service in Service.objects.filter(**kwargs):
            service.viewset.get_service.cache_clear()

    def get_for_viewset(self, viewset):
        return self.model.objects.get(viewset=viewset)

    def check_or_create(self, prefix, viewset, basename, url_name, ):
        name = getattr(viewset, 'label', viewset.__name__)
        source_model = ContentType.objects.get_for_model(viewset().get_queryset().model)
        service, isnew = self.model.objects.get_or_create(viewset=viewset,
                                                          defaults={
                                                              'name': name,
                                                              'cache_ttl': '1y',
                                                              'access': getattr(viewset, 'default_access',
                                                                                conf.DEFAULT_ACCESS),
                                                              'description': getattr(viewset, '__doc__', ""),
                                                              'source_model': source_model
                                                          })

        service.url_name = url_name
        service.basename = basename
        service.suffix = prefix
        service.source_model = source_model
        service.save()
        viewset.get_service.cache_clear()
        return service, isnew

    def load_services(self):
        router = conf.ROUTER
        created = deleted = 0
        list_name = router.routes[0].name
        for prefix, viewset, basename in router.registry:
            service, isnew = self.check_or_create(prefix, viewset, basename,
                                                  list_name.format(basename=basename))
            # try:
            if isnew:
                created += 1
            # except IntegrityError:
            #     service = self.model.objects.get(name=name)
            #     service.description = viewset.short_description

            # viewset.get_service.cache_clear()
            # service.viewset = viewset
            # service.save()

            # if viewset_fqn in manager:
            #     if not s.cache.refresh_function:
            #         refresh_function, ttl_green, ttl_red = manager[viewset_fqn]
            #         s.cache.refresh_function = fqn(refresh_function)
            #         s.cache.ttl_green = ttl_green
            #         s.cache.ttl_red = ttl_red
            #         s.cache.save()

        for service in self.model.objects.all():
            try:
                assert service.viewset
            except AssertionError:
                service.delete()
                deleted += 1

        return created, deleted, self.model.objects.count()


class Service(MasterDataModel):
    name = models.CharField(max_length=100, help_text='unique service name',
                            db_index=True, unique=True)
    description = models.TextField(blank=True, null=True)
    viewset = StrategyClassField(help_text='class FQN',
                                 unique=True, db_index=True)
    basename = models.CharField(max_length=200, help_text='viewset basename')
    suffix = models.CharField(max_length=200, help_text='url suffix')
    url_name = models.CharField(max_length=300, help_text='url name as per drf reverse')
    access = models.IntegerField(choices=[(k, v) for k, v in acl.ACL_LABELS.items()],
                                 default=acl.ACL_ACCESS_LOGIN,
                                 help_text="Required privileges")

    confidentiality = models.IntegerField(choices=acl.CONFIDENTIALITY_CHOICES,
                                          default=acl.CLASS_INTERNAL)

    hidden = models.BooleanField(default=False)

    cache_version = models.IntegerField(default=1)
    cache_ttl = models.CharField(default='1d', max_length=5)
    cache_key = models.CharField(max_length=1000,
                                 null=True, blank=True,
                                 help_text='Key used to invalidate service cache')

    source_model = models.ForeignKey(ContentType,
                                     models.CASCADE,
                                     blank=True,
                                     help_text="model used as primary datasource")

    linked_models = models.ManyToManyField(ContentType,
                                           related_name='+',
                                           blank=True,
                                           help_text="models that the service depends on")

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Services"

    objects = ServiceManager()

    def invalidate_cache(self):
        Service.objects.invalidate_cache(id=self.pk)
        self.refresh_from_db()
        return self.cache_version

    def reset_cache(self, value=0):
        Service.objects.filter(id=self.pk).update(cache_version=value)
        self.refresh_from_db()

    def get_access_level(self):
        # administrators cannot go lower than coded value
        return max(self.access, self.viewset.default_acl)

    @cached_property
    def endpoint(self):
        return reverse(f'api:{self.basename}-list', args=['latest'])

    @cached_property
    def display_name(self):
        return "{} ({})".format(self.viewset.__name__, self.viewset.source)

    def doc_url(self):
        base = '/api/+redoc/#operation/'
        path = self.suffix.replace('/', '_')
        return "{0}api_{1}_list".format(base, path)

    @cached_property
    def managed_model(self):
        try:
            return self.source_model.model_class()
        except TypeError:
            return None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            try:
                v = self.viewset()
                model = v.get_queryset().model
                ct = ContentType.objects.get_for_model(model)
                self.linked_models.add(ct)
            except Exception as e:
                logger.exception(e)
        super(Service, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class CacheVersion(Service):
    class Meta:
        proxy = True
