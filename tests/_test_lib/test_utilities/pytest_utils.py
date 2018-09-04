# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


class ArgsDecorator:
    """
        base class to create py.test markers on the fly using multiple arguments as Mark `names`

        How to use:
        1) create a concrete decorator with a unique PREFIX attribute

            class ticket(ArgsDecorator):
                PREFIX = 't'

        2) decorate your tests

            @ticket(320,500,600)
            def mytest():
                ...
                ...
        3) select your tests:
            py.test -m "t320 or t600"

    >>> @ticket(999)
    ... def test_example():
    ...   assert 1 == 1

    >>> @ticket(1000)
    ... class TestExample(object):
    ...   @ticket(1000, 1000)
    ...   def test_another1(self):
    ...     assert 2 == 2
    ...   def test_another2(self):
    ...     assert 3 == 3

    >>> @ticket(1001)
    ... class TestAnother(object):
    ...   def test_example(self): pass
    ...   def pytestmark(self): pass

    >>> @ticket(1002)
    ... class Test3(object):
    ...   pytestmark = []
    ...   def test_example(self): pass

    """
    PREFIX = None

    def __init__(self, *ids):
        self.markname = self.__class__.__name__
        self.tickets_id = ids
        self.args = ()
        self.kwargs = {}

    def __repr__(self):
        d = self.__dict__.copy()
        name = ','.join(d.pop('tickets_id'))
        return '<MarkDecorator %r %r>' % (name, d)

    def __call__(self, *args, **kwargs):
        """ if passed a single callable argument: decorate it with mark info.
            otherwise add *args/**kwargs in-place to mark information. """
        from _pytest.mark import Mark, MarkInfo
        if args:
            func = args[0]
            if len(args) == 1 and hasattr(func, '__call__') or \
                    hasattr(func, '__bases__'):
                if hasattr(func, '__bases__'):
                    if hasattr(func, 'pytestmark'):
                        markers = func.pytestmark
                        if not isinstance(markers, list):
                            func.pytestmark = [markers, self]
                        else:
                            markers.append(self)
                    else:
                        func.pytestmark = [self]
                else:
                    for x in self.tickets_id:
                        name = '%s%s' % (self.PREFIX, x)
                        holder = getattr(func, name, None)
                        mark = Mark(name, self.args, self.kwargs)
                        if holder is None:
                            holder = MarkInfo(mark)
                            setattr(func, name, holder)
                        else:
                            holder.add_mark(mark)
                return func
        kw = self.kwargs.copy()
        kw.update(kwargs)
        args = self.args + args
        return self.__class__(self.markname, args=args, kwargs=kw)


class ticket(ArgsDecorator):
    PREFIX = 't'
