from django.apps import AppConfig


def invalidate_cache(sender, **kwargs):
    for service in sender.linked_services:
        service.invalidate_cache()


class Config(AppConfig):
    name = "etools_datamart.apps.core"

    def ready(self):
        from etools_datamart.apps.etl.signals import data_refreshed

        data_refreshed.connect(invalidate_cache)
        from . import checks  # noqa
