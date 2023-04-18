import logging

from django.core.cache import cache

import requests
from unicef_security import config
from unicef_security.graph import AZURE_GRAPH_API_TOKEN_CACHE_KEY, Synchronizer

from etools_datamart.libs.version import get_full_version

logger = logging.getLogger(__name__)


class DatamartSynchronizer(Synchronizer):
    @property
    def token_key(self):
        return "%s:%s" % (AZURE_GRAPH_API_TOKEN_CACHE_KEY, get_full_version())

    def get_token(self):
        if not self.id and self.secret:
            raise ValueError("Configure AZURE_CLIENT_ID and/or AZURE_CLIENT_SECRET")
        token = cache.get(self.token_key)
        if not token:
            post_dict = {
                "grant_type": "client_credentials",
                "client_id": self.id,
                "client_secret": self.secret,
                "resource": config.AZURE_GRAPH_API_BASE_URL,
            }
            response = requests.post(config.AZURE_TOKEN_URL, post_dict)
            if response.status_code != 200:  # pragma: no cover
                logger.error(f"Unable to fetch token from Azure. {response.status_code} {response.content}")
                raise Exception(f"Error during token retrieval: {response.status_code} {response.content}")
            jresponse = response.json()
            token = jresponse["access_token"]
            # Cache token for 3600 seconds, which matches the default Azure token expiration
            cache.set(self.token_key, token, 3600)
        return token
