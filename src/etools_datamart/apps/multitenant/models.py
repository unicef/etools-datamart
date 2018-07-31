# -*- coding: utf-8 -*-
from django.db.models import *  # noqa


class TenantModel(Model):
    schema = CharField(db_column='__schema', max_length=100)

    class Meta:
        abstract = True
