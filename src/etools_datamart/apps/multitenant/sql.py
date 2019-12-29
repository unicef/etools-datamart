# -*- coding: utf-8 -*-
import re
from collections import OrderedDict

from django.utils.functional import cached_property

import sqlparse
from django_regex.utils import RegexList
from sqlparse.sql import Function, Identifier, IdentifierList, Where
from sqlparse.tokens import Keyword, Whitespace

SHARED_TABLES = RegexList(['"auth_.*',
                           '"publics_.*',
                           '"users_.*',
                           '"categories_.*',
                           '"django_content_type.*'
                           ])

cache = {}


def clean_stm(sql):
    return sql.replace("\n", " ").replace("\r", " ")


class Parser:
    def __init__(self, sql):
        self.raw_sql = self.original = clean_stm(sql)
        self.where = ""
        self._raw_tables = []
        # self._raw_order = []
        # self._raw_fields = []
        # self._raw_joins = []
        # self._raw_where = []
        self._unknown = []
        self._parsed = False
        self.clause = None
        self.is_count = False

    # @cached_property
    # def cleaned_order(self):
    #     ret = []
    #     for entry in self.raw_order:
    #         cleaned = entry.split(".")[-1]
    #         ret.append(cleaned)
    #     return ", ".join(ret)
    #
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
        raise AttributeError(item)  # pragma: no cover

    def split(self, stm):
        # TODO: improve regex
        _select = r'(?P<query>(?P<select>SELECT( DISTINCT)? )(?P<fields>.*))'
        _from = r'(?P<from> FROM (?P<tables>.*))'
        _where = r'(?P<where> WHERE .*)'
        _group = r'(?P<group> GROUP BY .*)'
        _order = r'(?P<order> ORDER BY .*)'
        _limit = r'(?P<limit> LIMIT .*)'

        rexx = [
            f"{_select}{_from}{_where}{_order}{_group}{_limit}",
            f"{_select}{_from}{_where}{_order}{_group}",
            f"{_select}{_from}{_where}{_group}",
            f"{_select}{_from}{_group}",
            f"{_select}{_from}{_group}{_limit}",
            f"{_select}{_from}{_order}{_group}",


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
            m = re.match(rex, stm, re.I + re.M)
            if m:
                self.parts = m.groupdict()
                return self.parts
        raise Exception(stm)  # pragma: no cover

    def join(self, parts):
        ret = ""
        for part in ['query', 'from', 'where', 'order']:
            ret += (parts.get(part, "") or "").rstrip()
        return ret

    def parse(self):  # noqa
        if self._parsed:  # pragma: no cover
            return
        target = self._unknown
        self.split(self.original)
        parsed = sqlparse.parse(self.original)
        self.tokens = parsed[0].tokens
        for token in self.tokens:
            value = token.value.upper()
            if token.value in ["SELECT", ]:
                self.clause = token.value
                continue
            if token.ttype in [Whitespace]:
                continue
            elif token.ttype is Keyword:
                if value in ['FROM', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'LEFT OUTER JOIN', 'RIGHT OUTER JOIN']:
                    target = self._raw_tables
                # elif value in ['SELECT', 'DISTINCT']:
                #     target = self._raw_fields
                # elif value in ['ON']:
                #     target = self._raw_joins
                # elif value in ['WHERE']:
                #     target = self._raw_where
                # elif value in ['ORDER', 'BY']:
                #     target = self._raw_order
                else:
                    target = self._unknown
            # elif token.ttype is Keyword.DML:
            #     target = self._raw_fields
            else:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        target.append(str(identifier))
                elif isinstance(token, Identifier):
                    self.is_count = self.is_count or 'COUNT(' in str(token)
                    target.append(str(token))
                # elif isinstance(token, Comparison):
                #     target.append(str(token))
                elif isinstance(token, Function):
                    self.is_count = self.is_count or 'COUNT(' in str(token)
                    target.append(str(token))
                elif isinstance(token, Where):
                    # target.append(str(token))
                    self.where = str(token)
                # elif token.ttype == Wildcard:
                #     target.append(str(token))
                # elif value in ["SELECT", "*"]:
                #     pass
                else:  # pragma: no cover
                    pass
                    # raise AttributeError(f"{token}: {type(token)} {value}")
        self._parsed = True

    def set_schema(self, schema, **overrides):
        if not self._parsed:
            self.parse()

        parts = dict(self.parts)
        if overrides:
            parts.update(overrides)

        _from = parts["from"].strip()
        for t in self.tables:
            if t in SHARED_TABLES:
                _from = _from.replace(t, f'"public".{t}')
            else:
                _from = _from.replace(t, f'"{schema}".{t}')

        ret = parts['select']
        self.mapping = OrderedDict()
        fields = parts['fields'].split(',')
        for field in fields:
            if '__schema' in field:
                self.mapping['schema'] = f"'{schema}' AS __schema"
            else:
                self.mapping[field] = re.sub(r'("(.[^"]*)"\."(.[^"]*)")', r'"\2"."\3" AS \2__\3', field)

        self.mapping['schema'] = f"'{schema}' AS __schema"

        ret += ", ".join(self.mapping.values())
        ret += f" {_from}"

        if self.where:
            ret += f" {parts['where']}"
        return ret

    def with_schemas(self, *schemas):
        if len(schemas) == 1:
            schema = schemas[0]
            ret = re.sub(r'".[^"]*"\."__schema"', f"'{schema}' AS __schema", self.original)
            return ret

        if not self._parsed:  # pragma: no cover
            self.parse()

        if self.is_count:
            ret = "SELECT COUNT(*) FROM ("
            ret += " UNION ALL ".join([self.set_schema(s, fields='id') for s in schemas])
            ret += ") as __count"
            return ret

        assert self.clause == "SELECT"
        ret = f"SELECT * FROM ("
        ret += " UNION ALL ".join([self.set_schema(s) for s in schemas])
        ret += ") as __query"
        if self.parts.get('order'):
            parts = self.parts.get('order').split(',')
            parts = map(lambda p: p.replace('"', '').replace(".", "__"), parts)
            ret += ",".join(parts)
        if self.parts.get('limit'):
            ret += f" {self.parts['limit']}"
        return ret
