from celery.app import default_app

from unicef_rest_framework.models import Service


@default_app.task()
def invalidate_cache(service_id):
    service = Service.objects.get(service_id)
    service.invalidate_cache()
    return {"cache_versipn": service.cache_version,
            "service": service.name}


@default_app.task()
def preload(service_id, querystring):
    service = Service.objects.get(service_id)
    service.invalidate_cache()
    return {"cache_versipn": service.cache_version,
            "service": service.name}
