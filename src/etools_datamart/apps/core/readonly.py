# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.db import models

logger = logging.getLogger(__name__)


class ReadOnlyManager(models.Manager):
    def create(self, **kwargs):
        pass

    def get_or_create(self, defaults=None, **kwargs):
        pass

    def update_or_create(self, defaults=None, **kwargs):
        pass

    def _extract_model_params(self, defaults, **kwargs):
        pass

    def delete(self):
        pass

    def _raw_delete(self, using):
        pass

    def update(self, **kwargs):
        pass

    def _update(self, values):
        pass

    def raw(self, raw_query, params=None, translations=None, using=None):
        pass

    def select_for_update(self, nowait=False):
        pass

    def _insert(self, objs, fields, return_id=False, raw=False, using=None):
        pass

    def _batched_insert(self, objs, fields, batch_size):
        pass


class ReadOnlyModel(models.Model):
    objects = ReadOnlyManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        pass

    def delete(self, using=None, keep_parents=False):
        super(ReadOnlyModel, self).delete(using)

    class Meta:
        abstract = True
