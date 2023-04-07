from django.apps import AppConfig


class Config(AppConfig):
    name = "unicef_rest_framework"
    verbose_name = "API Configuration"

    def ready(self):
        from . import handlers  # noqa
        from . import tasks  # noqa
