# -*- coding: utf-8
from django.apps import AppConfig


class Config(AppConfig):
    name = 'core'

    def ready(self):
        super().ready()
