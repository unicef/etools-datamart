import re

from .exceptions import InvalidPattern, InvalidQueryValueError


def parse_bool(value):
    if str(value).lower() in ["true", "1", "yes", "t", "y", "on"]:
        return True
    elif str(value).lower() in ["false", "0", "no", "f", "n"]:
        return False
    else:
        raise InvalidQueryValueError(value)


class RexList(list):
    """
        list class where each entry is a valid regular expression

    >>> r = RexList(["a.*"])
    >>> r.append("[0-9]*")
    >>> "1" in r
    True

    >>> "cc" in r
    False

    >>> "abc" in r
    True

    >>> print(r)
    [u'a.*', u'[0-9]*']

    >>> r[0] = '.*'

    >>> r[0] = '[0-'
    Traceback (most recent call last):
        ...
    InvalidPattern: [0- is not a valid regular expression
    """

    def __init__(self, seq=None):
        regexx = []
        if seq:
            for el in seq:
                regexx.append(self._compile(el))
        super().__init__(regexx)

    def __repr__(self):
        return str([r.pattern for r in self])

    def _compile(self, pattern, index=None):
        try:
            return re.compile(pattern)
        except (TypeError, re.error):
            raise InvalidPattern(pattern)

    def __setitem__(self, i, pattern):
        rex = self._compile(pattern)
        super().__setitem__(i, rex)

    def append(self, pattern):
        rex = self._compile(pattern)
        super().append(rex)

    def __contains__(self, target):
        t = str(target)
        for rex in self:
            m = rex.match(t)
            if m and m.group():
                return True
        return False
