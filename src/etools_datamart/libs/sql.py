# -*- coding: utf-8 -*-
import re

import sqlparse
from django.utils.functional import cached_property, Promise
from django_regex.utils import RegexList
from sqlparse.sql import Comparison, Identifier, IdentifierList, Parenthesis, Where, Function
from sqlparse.tokens import Keyword, Whitespace, Wildcard

SHARED_TABLES = RegexList(['"auth_.*',])


class RawSql(str):
    """
    A str subclass that has been specifically marked as "raw"
    skip any tenant related manipulation
    """

    def __add__(self, rhs):
        """
        Concatenating a raw string with another string
        Otherwise, the result is no longer safe.
        """
        t = super().__add__(rhs)
        if isinstance(rhs, RawSql):
            return RawSql(t)
        return t

    def __str__(self):
        return self


def raw_sql(s):
    """
    Explicitly mark a string as raw sql. The returned
    object can be used everywhere a string is appropriate.

    Can be called multiple times on a single string.
    """
    if isinstance(s, (str, Promise)):
        return RawSql(s)
    return RawSql(str(s))


class Parser:
    def __init__(self, sql):
        self.raw_sql = sql
        self.sql = sql
        self.where = ""
        self._raw_tables = []
        self._raw_order = []
        self._raw_fields = []
        self._raw_joins = []
        self._raw_where = []
        self._unknown = []
        self._parsed = False

        self.is_count = False

    # @cached_property
    # def order(self):
    #     return [s.replace(" ASC", "").replace(" DESC", "").replace('"','') for s in self.raw_order]

    @cached_property
    def cleaned_order(self):
        ret = []
        for entry in self.raw_order:
            cleaned = entry.split(".")[-1]
            ret.append(cleaned)
        return ", ".join(ret)

    @cached_property
    def fields(self):
        ret = []
        for name in self.raw_fields:
            # name = name.replace('"', '')
            if " AS " in name:
                ret.append(name.split(" AS ")[-1])
            elif "." in name:
                ret.append(name.split(".")[-1])
            else:
                ret.append(name)
        return ret

    @cached_property
    def tables(self):
        ret = []
        for name in self.raw_tables:
            # name = name.replace('"', '')
            if "." in name:
                ret.append(name.split(".")[-1])
            else:
                ret.append(name)
        return ret

    def __getattr__(self, item):
        if item in ['raw_tables', 'raw_order', 'raw_fields', 'raw_joins', 'raw_where', 'unknown']:
            if not self._parsed:
                self.parse()
            return getattr(self, f'_{item}')
        raise AttributeError(item)

    def split(self, stm):
        _select = '(?P<select>SELECT( DISTINCT)? (?P<fields>.*))'
        _from = '(?P<from> FROM (?P<tables>.*))'
        _where = '(?P<where> WHERE .*)'
        _order = '(?P<order> ORDER BY .*)'

        rexx = [
            f"{_select}{_from}{_where}{_order}",
            f"{_select}{_from}{_order}",
            f"{_select}{_from}{_where}",
            f"{_select}{_from}",
            # '(?P<select>SELECT( DISTINCT)?) (?P<fields>.*) (?P<from>FROM (?P<tables>.*)) WHERE (?P<where>.*) ORDER BY (?P<order>.*)',
            # '(?P<select>SELECT( DISTINCT)?) (?P<fields>.*) (?P<from>FROM (?P<tables>.*)) ORDER BY (?P<order>.*)',
            # '(?P<select>SELECT( DISTINCT)?) (?P<fields>.*) (?P<from>FROM (?P<tables>.*)) WHERE (?P<where>.*)',
            # '(?P<select>SELECT( DISTINCT)?) (?P<fields>.*) (?P<from>FROM (?P<tables>.*))'
        ]
        for rex in rexx:
            m = re.match(rex, stm, re.I)
            if m:
                self.parts = m.groupdict()
                return self.parts
        raise Exception(stm)

    def join(self, parts):
        ret = ""
        for part in ['select', 'from', 'where', 'order']:
            ret += (parts.get(part, "") or "").rstrip()
        return ret

    def parse(self):
        if self._parsed:
            return
        target = self._unknown
        self.split(self.sql)
        parsed = sqlparse.parse(self.sql)
        self.tokens = parsed[0].tokens
        for token in self.tokens:
            if token.ttype in [Whitespace]:
                continue
            elif token.ttype is Keyword:
                value = token.value.upper()
                if value in ['SELECT', 'DISTINCT']:
                    target = self._raw_fields
                elif value in ['FROM', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'LEFT OUTER JOIN', 'RIGHT OUTER JOIN']:
                    target = self._raw_tables
                elif value in ['ON']:
                    target = self._raw_joins
                elif value in ['WHERE']:
                    target = self._raw_where
                elif value in ['ORDER', 'BY']:
                    target = self._raw_order
                else:
                    target = self._unknown
            elif token.ttype is Keyword.DML:
                target = self._raw_fields
            else:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        target.append(str(identifier))
                elif isinstance(token, Identifier):
                    if 'COUNT(*)' in str(token):
                        self.is_count = True
                    target.append(str(token))
                elif isinstance(token, Comparison):
                    target.append(str(token))
                elif isinstance(token, Function):
                    if 'COUNT(*)' in str(token):
                        self.is_count = True
                    target.append(str(token))
                elif isinstance(token, Where):
                    # target.append(str(token))
                    self.where = str(token)
                elif token.ttype == Wildcard:
                    target.append(str(token))
                else:
                    pass
                    # raise AttributeError(type(token))
        self._parsed = True

    # def set_schema(self, schema, target=None):
    #     if not self._parsed:
    #         self.parse()
    #     ret = target or self.sql
    #     for t in self.tables:
    #         if t in SHARED_TABLES:
    #             ret = ret.replace(t, f'"public".{t}')
    #         else:
    #             ret = ret.replace(f" {t}", f' "{schema}".{t}')
    #     return ret

    def set_schema2(self, schema, **overrides):
        if not self._parsed:
            self.parse()

        parts = dict(self.parts)
        if overrides:
            parts.update(overrides)

        _f = parts["from"].strip()
        for t in self.tables:
            if t in SHARED_TABLES:
                _f = _f.replace(t, f'"public".{t}')
            else:
                _f = _f.replace(t, f'"{schema}".{t}')

        ret = f'{parts["select"].strip()}, \'{schema}\' AS __schema {_f}'
        if self.where:
            ret += f" {parts['where']}"
        return ret

    def with_schemas(self, *schemas):
        if not self._parsed:
            self.parse()
        # sql = self.sql
        if self.is_count:
            # base = f"SELECT id FROM {','.join(self.tables)}"
            ret = "SELECT count(id) FROM ("
            ret += " UNION ALL ".join([self.set_schema2(s, select='SELECT id') for s in schemas])
            ret += ") as __count"
            return ret
        if len(schemas) == 1:
            return self.set_schema(schemas[0])
        else:
            # def listify(fields):
            #     return ",".join(['%s' % f for f in fields])

            # base = f'{self.parts["select"].strip()}, \'==SCHEMA==\' AS __schema {self.parts["from"].strip()}'
            # base = f'SELECT \'==SCHEMA==\' AS __schema, {listify(self._raw_fields)} FROM {",".join(self.tables)}'
            # if self.where:
            #     base += f" {self.parts['where']}"

            ret = f"SELECT {', '.join(self.fields)} FROM ("
            # ret += " UNION ALL ".join([self.set_schema(s, base).replace("==SCHEMA==", s) for s in schemas])
            ret += " UNION ALL ".join([self.set_schema2(s) for s in schemas])
            ret += ") as __query"
            if self.parts.get('order'):
                ret += f" ORDER BY {self.cleaned_order}"
            return ret


def make_multitenant(sql):
    pass


if __name__ == "__main__":

    sqls = [
        '''SELECT f1 FROM t1''',
        '''SELECT DISTINCT f1 FROM t1''',
        '''SELECT f1 FROM t1 ORDER BY o1''',
        '''SELECT "f1" FROM "t1" ORDER BY "o1" ASC''',
        '''SELECT DISTINCT "f1" FROM "t1" ORDER BY "o1" ASC''',
        '''SELECT DISTINCT "t1"."f1" FROM "t1" ORDER BY "o1" ASC''',
        '''SELECT DISTINCT "t1"."f1" FROM "t1" ORDER BY "t1"."f1" ASC''',
        '''SELECT DISTINCT "s1"."t1"."f1" FROM "t1" ORDER BY "t1"."f1" ASC''',
        '''SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" INNER JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC''',
    ]
    for sql in sqls[1:]:
        parser = Parser(sql)
        print(parser.sql)
        assert parser.tables == ["t1"], parser.tables
        assert parser.order == ["o1 ASC"], parser.order
        assert parser.order_fields == ["o1"], parser.order_fields
        # FIXME: remove me (print)
        # for t in parser.tokens:
        #     if t.ttype != Whitespace:
        #         print(f"{type(t)}   {t.ttype} {t}")
        print("-" * 80)
