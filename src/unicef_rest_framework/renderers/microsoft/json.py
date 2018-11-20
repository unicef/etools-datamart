import json

from rest_framework.compat import SHORT_SEPARATORS
from rest_framework.renderers import JSONRenderer


class MSJSONRenderer(JSONRenderer):
    media_type = 'application/json'
    format = 'ms-json'
    disable_pagination = True

    def render(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context['view']
        data = {f"{view.__class__.__name__}_JSONResult": json.dumps(data)}
        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=0, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=SHORT_SEPARATORS
        )
        return bytes(ret.encode('utf-8'))
