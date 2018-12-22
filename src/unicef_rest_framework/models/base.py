# -*- coding: utf-8 -*-

import logging
import uuid

from django.conf import settings
from django.db import models
from django.db.models import UUIDField
from django.utils.translation import ugettext_lazy as _

from concurrency.fields import IntegerVersionField

logger = logging.getLogger(__name__)


class MasterDataModel(models.Model):
    version = IntegerVersionField()
    uuid = UUIDField(unique=True, default=uuid.uuid4,
                     editable=False,
                     help_text=_('Unique identifier'))
    last_modify_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         editable=False,
                                         related_name='+',
                                         blank=True, null=True,
                                         on_delete=models.SET_NULL)
    last_modify_date = models.DateTimeField(auto_now=True,
                                            editable=False,)

    class Meta:
        abstract = True
