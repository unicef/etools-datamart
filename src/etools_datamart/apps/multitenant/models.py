# -*- coding: utf-8 -*-

from django.db.models import *  # noqa
from django.db.models.manager import BaseManager

from .query import TenantQuerySet


class TenantManager(BaseManager.from_queryset(TenantQuerySet)):
    pass


class TenantModel(Model):  # noqa
    schema = CharField(db_column='__schema', max_length=100)  # noqa

    objects = TenantManager()

    class Meta:
        abstract = True
