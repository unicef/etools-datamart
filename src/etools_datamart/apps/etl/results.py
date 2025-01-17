import json
from json.decoder import WHITESPACE

from rest_framework.utils import encoders


class EtlDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        return super().decode(s, _w)


class EtlEncoder(encoders.JSONEncoder):
    def default(self, obj):
        from etools_datamart.apps.etl.loader import EtlResult

        if isinstance(obj, EtlResult):
            return {"__type__": "__EtlResult__", "data": obj.as_dict()}
        return super().default(obj)


def etl_decoder(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__EtlResult__":  # pragma: no cover
            from etools_datamart.apps.etl.loader import EtlResult

            return EtlResult(**obj["data"])
    return obj


#
# Encoder function
def etl_dumps(obj):
    return json.dumps(obj, cls=EtlEncoder)


#
#
# # Decoder function
def etl_loads(obj):
    return json.loads(obj, cls=EtlDecoder, object_hook=etl_decoder)
