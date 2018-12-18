from constance import config

from etools_datamart.libs.version import get_full_version


def get_cache_key(name, *args):
    return f"{name}:{get_full_version()}:{config.CACHE_VERSION}:{':'.join(map(str,args))}"
