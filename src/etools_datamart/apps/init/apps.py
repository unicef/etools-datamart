from django.apps import AppConfig


class Config(AppConfig):
    name = "etools_datamart.apps.init"

    def ready(self):
        from . import checks  # noqa
