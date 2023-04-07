from _decimal import Decimal


class SafeDecimal(Decimal):
    def __new__(cls, value="0", context=None):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            value = str(value)
        if isinstance(value, str) and "," in value:
            value = value.replace(",", ".")
        value = value.rstrip("0").rstrip(".") if "." in value else value
        return Decimal.__new__(cls, value, context)

    def _validate_for_field(self, field):
        for v in field.validators:
            v(self)
