import crashlog.middleware
from django.apps import AppConfig
from django.core.signals import got_request_exception


class Config(AppConfig):
    def ready(self):
        got_request_exception.connect(crashlog.middleware.process_exception)
