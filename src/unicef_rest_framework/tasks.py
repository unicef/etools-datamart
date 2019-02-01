import logging

from django.conf import settings
from django.contrib.auth import get_user_model

import requests
from celery.app import default_app

from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)


@default_app.task()
def invalidate_cache(service_id):
    service = Service.objects.get(service_id)
    service.invalidate_cache()
    return {"cache_versipn": service.cache_version,
            "service": service.name}


@default_app.task()
def preload(path):
    User = get_user_model()
    user = User.objects.get(username='system')
    target = "%s%s" % (settings.ABSOLUTE_BASE_URL, path)
    logger.info(f'Preloading {target}')
    assert path.startswith('/')
    response = requests.get(target,
                            headers={'Authorization': 'Token %s' % user.auth_token})
    return response.headers
