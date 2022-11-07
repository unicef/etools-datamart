import hashlib

from rest_framework_extensions.key_constructor.bits import KeyBitBase

from etools_datamart.api.filtering import CountryFilter
from etools_datamart.apps.security.utils import get_allowed_schemas


class SchemaAccessKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        value = ""
        if request.user.is_authenticated:
            if CountryFilter.query_param not in request.GET:
                value = get_allowed_schemas(request.user)

        hashed_value = hashlib.md5(str(value).encode()).hexdigest()
        return {'countries': hashed_value}
