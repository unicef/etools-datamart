# -*- coding: utf-8 -*-
import sqlparse
from django.utils.functional import cached_property
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, Whitespace

SHARED_TABLES = ['"auth_group"', ]

import sqlparse
from sqlparse.sql import Where, Comparison, Parenthesis, Identifier


class Parser:
    def __init__(self, sql):
        self.raw_sql = sql
        self.sql = sql.replace('"', '')
        self._raw_tables = []
        self._raw_order = []
        self._raw_fields = []
        self._unknown = []
        self._parsed = False

    @cached_property
    def order(self):
        return [s.replace(" ASC", "").replace(" DESC", "") for s in self.raw_order]

    @cached_property
    def fields(self):
        ret = []
        for name in self.raw_fields:
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
            if "." in name:
               ret.append(name.split(".")[-1])
            else:
                ret.append(name)
        return ret

    def __getattr__(self, item):
        if item in ['raw_tables', 'raw_order', 'raw_fields', 'unknown']:
            if not self._parsed:
                self.parse()
            return getattr(self, f'_{item}')
        raise AttributeError(item)


    def parse(self):
        target = self._unknown
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
                elif value in ['ORDER', 'BY']:
                    target = self._raw_order
                else:
                    target = self._unknown
                # continue
            elif token.ttype is Keyword.DML:
                target = self._raw_fields
                # continue
            else:
            # if seen:
                # if token.ttype is Keyword:
                #     continue
                # else:
                    if isinstance(token, IdentifierList):
                        for identifier in token.get_identifiers():
                            target.append(str(identifier))
                    elif isinstance(token, Identifier):
                        target.append(str(token))
                    else:
                        pass
            # if token.ttype is Keyword and token.value.upper() == "FROM":
            #     from_seen = True
        self._parsed = True
    # @cached_property
    # def tables(self):
    #     tables = []
    #     from_seen = False
    #     for token in self.tokens:
    #         if token.ttype is Keyword and token.value.upper() == "ORDER":
    #             break
    #         if from_seen:
    #             if token.ttype is Keyword:
    #                 continue
    #             else:
    #                 if isinstance(token, IdentifierList):
    #                     for identifier in token.get_identifiers():
    #                         tables.append(str(identifier))
    #                 elif isinstance(token, Identifier):
    #                     tables.append(str(token))
    #                 else:
    #                     pass
    #         if token.ttype is Keyword and token.value.upper() == "FROM":
    #             from_seen = True
    #     return tables


def get_tables(sql):
    sql = sql.replace('"', '')
    tables = []
    parsed = sqlparse.parse(sql)
    stmt = parsed[0]
    from_seen = False
    for token in stmt.tokens:
        if token.ttype is Keyword and token.value.upper() == "ORDER":
            break
        if from_seen:
            if token.ttype is Keyword:
                continue
            else:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        tables.append(str(identifier))
                elif isinstance(token, Identifier):
                    tables.append(str(token))
                else:
                    pass
        if token.ttype is Keyword and token.value.upper() == "FROM":
            from_seen = True
    return tables


def add_schema(statement, schema):
    tables = get_tables(statement)
    ret = statement
    for t in tables:
        if t in SHARED_TABLES:
            ret = ret.replace(t, f'"public".{t}')
        else:
            ret = ret.replace(f" {t}", f' "{schema}".{t}')
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
