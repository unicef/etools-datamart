from django.apps import AppConfig


class Config(AppConfig):
    name = "etools_datamart.apps.mart.data"
    verbose_name = "eTools"

    def ready(self):
        from . import checks  # noqa
