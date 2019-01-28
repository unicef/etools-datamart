from django.core import checks
from django.core.checks import INFO, Warning


@checks.register()
def check_services(app_configs, **kwargs):
    from unicef_rest_framework.models import Service
    created, deleted, total = Service.objects.load_services()
    if created:
        return [Warning(INFO, f"{created} new services found")]
    return []
