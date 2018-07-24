# -*- coding: utf-8
from django.apps import AppConfig
from django.db.backends.signals import connection_created
from etools_datamart.libs.schema import set_search_path


class Config(AppConfig):
    name = 'core'

    def ready(self):
        super().ready()
