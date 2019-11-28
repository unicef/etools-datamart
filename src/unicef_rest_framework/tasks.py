import logging

from celery.app import default_app
from post_office import mail

from unicef_rest_framework.models import Export, Preload, Service

logger = logging.getLogger(__name__)


@default_app.task()
def invalidate_cache(service_id):
    service = Service.objects.get(service_id)
    service.invalidate_cache()
    return {"cache_versipn": service.cache_version,
            "service": service.name}


@default_app.task()
def preload_all():
    for t in Preload.objects.filter(enabled=True).values_list('id', flat=True):
        preload.apply_async(args=[t])

    for t in Export.objects.filter(enabled=True, refresh=True).values_list('id', flat=True):
        preload.apply_async(args=[t])


@default_app.task()
def preload(target_id):
    target = Preload.objects.get(id=target_id)
    response = target.run()
    return response.status_code


@default_app.task()
def export(target_id):
    target = Export.objects.get(id=target_id)
    response = target.run()
    if target.as_user.email:
        mail.send(
            target.as_user.email,  # List of email addresses also accepted
            'notification@datamart.unicef.io',
            template='export_ready',
            context={'target': target, },
            attachments=[target.content]
        )
    return response.status_code
