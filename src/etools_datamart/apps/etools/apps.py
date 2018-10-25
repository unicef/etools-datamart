from functools import partial, partialmethod

from django.apps import AppConfig


def label(attr, self):
    return getattr(self, attr)


class Config(AppConfig):
    name = 'etools_datamart.apps.etools'
    verbose_name = "eTools"

    def ready(self):

        # from django.apps import get_app, get_models
        from django.apps import apps

        app_models = apps.get_app_config('etools').get_models()
        for model in app_models:
            for attr in ['name', 'username']:
                if hasattr(model, attr):
                    setattr(model, '__str__', partialmethod(partial(label, attr)))
                    break
