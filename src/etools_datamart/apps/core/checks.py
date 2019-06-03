import sys

from django.core import checks


@checks.register()
def check_services(app_configs, **kwargs):
    from unicef_rest_framework.models import Service
    created, deleted, total = Service.objects.load_services()
    sys.stdout.write(f"{total} services found. {created} new. {deleted} deleted")
    return []
