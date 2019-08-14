from django.apps import AppConfig


class Config(AppConfig):
    name = 'etools_datamart.apps.prp'
    verbose_name = "PRP"
    label = 'prp'

    def ready(self):
        pass
