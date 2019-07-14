import decimal
import json
import sys

from pygments import formatters, highlight, lexers


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def print(obj, *args):
    if isinstance(obj, (dict, list, tuple)):
        formatted_json = json.dumps(obj, sort_keys=True, indent=4, cls=DecimalEncoder)
    else:
        formatted_json = str(obj)

    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    out = " ".join([colorful_json] + list(map(str, args)))
    sys.stdout.write("%s\n" % out)
