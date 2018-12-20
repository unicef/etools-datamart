import json
#
from json.decoder import WHITESPACE

from rest_framework.utils import encoders


# CREATED = 'created'
# UPDATED = 'updated'
# UNCHANGED = 'unchanged'
#
#
# class EtlResult:
#     __slots__ = [CREATED, UPDATED, UNCHANGED]
#
#     def __init__(self, updated=0, created=0, unchanged=0, **kwargs):
#         self.created = created
#         self.updated = updated
#         self.unchanged = unchanged
#
#     def __repr__(self):
#         return repr(self.as_dict())
#
#     def incr(self, counter):
#         setattr(self, counter, getattr(self, counter) + 1)
#
#     def as_dict(self):
#         return {'created': self.created,
#                 'updated': self.updated,
#                 'unchanged': self.unchanged}
#
#     def __eq__(self, other):
#         # FIXME: pdb
#         import pdb; pdb.set_trace()
#         if isinstance(other, EtlResult):
#             other = other.as_dict()
#
#         if isinstance(other, dict):
#             return (self.created == other['created'] and
#                     self.updated == other['updated'] and
#                     self.unchanged == other['unchanged'])
#         return False
#
#
class EtlDecoder(json.JSONDecoder):

    def decode(self, s, _w=WHITESPACE.match):
        return super().decode(s, _w)


class EtlEncoder(encoders.JSONEncoder):

    def default(self, obj):
        from etools_datamart.apps.data.loader import EtlResult
        if isinstance(obj, EtlResult):
            return {
                '__type__': '__EtlResult__',
                'data': obj.as_dict()
            }
        return super(EtlEncoder, self).default(obj)


def etl_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__EtlResult__':
            from etools_datamart.apps.data.loader import EtlResult
            return EtlResult(**obj['data'])
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
