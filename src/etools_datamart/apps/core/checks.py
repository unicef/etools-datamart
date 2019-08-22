from django.core import checks

# from django.core.checks import Error


@checks.register()
def check_loader(app_configs, **kwargs):
    errors = []
    return errors
