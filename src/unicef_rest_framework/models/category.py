# -*- coding: utf-8 -*-

import logging

from django.db import models

from .base import MasterDataModel

logger = logging.getLogger(__name__)


class Category(MasterDataModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)
