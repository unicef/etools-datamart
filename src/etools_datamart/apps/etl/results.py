import json

CREATED = 'created'
UPDATED = 'updated'
UNCHANGED = 'unchanged'


class EtlResult:
    __slots__ = [CREATED, UPDATED, UNCHANGED]

    def __init__(self, updated=0, created=0, unchanged=0, **kwargs):
        self.created = created
        self.updated = updated
        self.unchanged = unchanged

    def __repr__(self):
        return repr(self.as_dict())

    def incr(self, counter):
        setattr(self, counter, getattr(self, counter) + 1)

    def as_dict(self):
        return {'created': self.created,
                'updated': self.updated,
                'unchanged': self.unchanged}

    def __eq__(self, other):
        if isinstance(other, EtlResult):
            other = other.as_dict()

        if isinstance(other, dict):
            return (self.created == other['created'] and
                    self.updated == other['updated'] and
                    self.unchanged == other['unchanged'])
        return False


class EtlEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EtlResult):
            return {
                '__type__': '__EtlResult__',
                'data': obj.as_dict()
            }
        else:
            return json.JSONEncoder.default(self, obj)


def etl_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__EtlResult__':
            return EtlResult(**obj)
    return obj


# Encoder function
def etl_dumps(obj):
    return json.dumps(obj, cls=EtlEncoder)


# Decoder function
def etl_loads(obj):
    return json.loads(obj, object_hook=etl_decoder)
