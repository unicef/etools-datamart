# -*- coding: utf-8 -*-
import re
from collections import OrderedDict

import sqlparse
from django.utils.functional import cached_property
from django_regex.utils import RegexList
from sqlparse.sql import Comparison, Function, Identifier, IdentifierList, Where
from sqlparse.tokens import Keyword, Whitespace, Wildcard

SHARED_TABLES = RegexList(['"auth_.*',
                           '"publics_.*',
                           '"users_.*',
                           ])

cache = {}


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

    @cached_property
    def cleaned_order(self):
        ret = []
        for entry in self.raw_order:
            cleaned = entry.split(".")[-1]
            ret.append(cleaned)
        return ", ".join(ret)

    # @cached_property
    # def fields(self):
    #     ret = []
    #     for name in self.raw_fields:
    #         # name = name.replace('"', '')
    #         # if " AS " in name:
    #         #     ret.append(name.split(" AS ")[-1])
    #         # elif "." in name:
    #         #     ret.append(name.split(".")[-1])
    #         # else:
    #         ret.append(name)
    #     return ret

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
        # TODO: improve regex
        _select = r'(?P<query>(?P<select>SELECT( DISTINCT)? )(?P<fields>.*))'
        _from = r'(?P<from> FROM (?P<tables>.*))'
        _where = r'(?P<where> WHERE .*)'
        _order = r'(?P<order> ORDER BY .*)'
        _limit = r'(?P<limit> LIMIT .*)'

        rexx = [
            f"{_select}{_from}{_where}{_order}{_limit}",
            f"{_select}{_from}{_where}{_order}",
            f"{_select}{_from}{_order}{_limit}",
            f"{_select}{_from}{_order}",
            f"{_select}{_from}{_where}{_limit}",
            f"{_select}{_from}{_where}",
            f"{_select}{_from}{_limit}",
            f"{_select}{_from}",
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

    def parse(self):  # noqa
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

    def set_schema(self, schema, **overrides):
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

        ret = self.parts['select']
        self.mapping = OrderedDict()
        for field in self.raw_fields:
            if '__schema' in field:
                self.mapping['schema'] = f"'{schema}' AS __schema"
            else:
                self.mapping[field] = re.sub(r'("(.[^"]*)"\."(.[^"]*)")', r'"\2"."\3" AS \2__\3', field)

        ret += ", ".join(self.mapping.values())
        ret += f" {_f}"
        if '__schema' not in ret:
            ret = f'{parts["select"].strip()}, \'{schema}\' AS __schema {_f}'

        if self.where:
            ret += f" {parts['where']}"
        return ret

    def with_schemas(self, *schemas):
        if len(schemas) == 1:
            schema = schemas[0]
            ret = re.sub(r'".[^"]*"\."__schema"', f"'{schema}' AS __schema", self.sql)
            return ret

        if not self._parsed:
            self.parse()
        if self.is_count:
            ret = "SELECT COUNT(id) FROM ("
            ret += " UNION ALL ".join([self.set_schema(s, select='SELECT id') for s in schemas])
            ret += ") as __count"
            return ret
        if len(schemas) == 1:
            return self.set_schema(schemas[0])
        else:
            ret = f"SELECT * FROM ("
            ret += " UNION ALL ".join([self.set_schema(s) for s in schemas])
            ret += ") as __query"
            if self.parts.get('order'):
                base = self.parts.get('order')
                for part in base.split(","):
                    ret += part.replace('"','').replace(".", "__")
            if self.parts.get('limit'):
                ret += f" {self.parts['limit']}"
            return ret
