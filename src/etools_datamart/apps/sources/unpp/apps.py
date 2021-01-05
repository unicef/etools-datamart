from django.apps import AppConfig


class Config(AppConfig):
    name = 'etools_datamart.apps.sources.unpp'
    verbose_name = "UNPP"
    label = 'source_unpp'

    def ready(self):
        pass
        # from .enrichment import patch
        # patch()
