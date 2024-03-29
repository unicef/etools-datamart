import json
import logging
from collections.abc import Iterable, MutableMapping
from typing import Any

from drf_excel import fields
from drf_excel.renderers import XLSXRenderer as _XLSXRenderer

from unicef_rest_framework.renderers.mixin import ContentDispositionMixin

logger = logging.getLogger(__name__)


# patch of XLSXListField.prep_value() to handle None values
# known issue https://github.com/wharton/drf-excel/issues/61
def patched_prep_value(self) -> Any:
    if self.value is None:
        return None
    if len(self.value) > 0 and isinstance(self.value[0], Iterable):
        # array of array; write as json
        return json.dumps(self.value, ensure_ascii=False)
    else:
        # Flatten the array into a comma separated string to fit
        # in a single spreadsheet column
        return self.list_sep.join(map(str, self.value))


fields.XLSXListField.prep_value = patched_prep_value


class XLSXRenderer(ContentDispositionMixin, _XLSXRenderer):
    def _flatten(self, data, parent_key="", key_sep=".", list_sep=", "):
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{key_sep}{k}" if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(self._flatten(v, new_key, key_sep=key_sep).items())
            elif isinstance(v, Iterable) and not isinstance(v, str):
                # Flatten the array into a comma separated string to fit
                # in a single spreadsheet column
                vv = []
                for item in v:
                    if isinstance(item, dict):
                        vv.append("\n".join([f"{ki}: {vi}" for ki, vi in item.items() if vi]))
                    elif isinstance(item, list):
                        vv.append(": ".join(item))
                    else:
                        vv.append(item)
                items.append((new_key, list_sep.join(vv)))
            else:
                items.append((new_key, v))
        return dict(items)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]
        self.process_response(renderer_context)
        if response.status_code == 200 and data:
            try:
                return super().render(data, accepted_media_type, renderer_context)

            except Exception as e:
                logger.exception(e)
                raise Exception(f"Error processing request {e}") from e
        else:
            return ""
