from django.apps import AppConfig


class Config(AppConfig):
    name = "etools_datamart.apps.sources.source_prp"
    verbose_name = "PRP"
    label = "source_prp"

    def ready(self):
        from .enrichment import patch

        patch()
