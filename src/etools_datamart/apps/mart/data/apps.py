# -*- coding: utf-8 -*-
from django.apps import AppConfig


class Config(AppConfig):
    name = 'etools_datamart.apps.mart.data'

    def ready(self):
        from . import checks  # noqa
