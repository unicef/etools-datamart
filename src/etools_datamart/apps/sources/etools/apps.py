from django.apps import AppConfig


class Config(AppConfig):
    name = "etools_datamart.apps.sources.etools"
    verbose_name = "eTools"

    def ready(self):
        from .enrichment import apply

        apply()
