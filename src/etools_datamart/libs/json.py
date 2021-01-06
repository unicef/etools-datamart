import decimal
import json
import sys
from datetime import datetime

from pygments import formatters, highlight, lexers


class SmartEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, (datetime,)):
            return str(o)
        return super().default(o)


def print_json(obj, *args):
    if isinstance(obj, (dict, list, tuple)):
        formatted_json = json.dumps(obj, sort_keys=True, indent=4, cls=SmartEncoder)
    else:
        formatted_json = str(obj)

    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    out = " ".join([colorful_json] + list(map(str, args)))
    sys.stdout.write("%s\n" % out)
