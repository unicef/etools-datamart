from _decimal import Decimal


class SafeDecimal(Decimal):

    def __new__(cls, value="0", context=None):
        if value is None:
            return None
        if isinstance(value, str) and ',' in value:
            value = value.replace(',', '.')
        return Decimal.__new__(cls, value, context)
