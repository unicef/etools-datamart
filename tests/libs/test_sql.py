# -*- coding: utf-8 -*-
import pytest

from etools_datamart.libs.sql import get_tables, add_schema, Parser

one_table = [
    # 'SELECT * FROM t1',
    'SELECT f1 AS f1 FROM t1',
    'SELECT f1 FROM t1',
    'SELECT DISTINCT f1 FROM t1',
    'SELECT f1 FROM t1 ORDER BY o1',
    'SELECT "f1" FROM "t1" ORDER BY "o1" ASC',
    'SELECT DISTINCT "f1" FROM "t1" ORDER BY "o1" ASC',
    'SELECT DISTINCT "t1"."f1" FROM "t1" ORDER BY "o1" ASC',
    'SELECT DISTINCT "t1"."f1" FROM "t1" ORDER BY "t1"."f1" ASC',
    'SELECT DISTINCT "s1"."t1"."f1" FROM "s1"."t1" ORDER BY "t1"."f1" ASC',
    'SELECT DISTINCT "s1"."t1"."f1" FROM "t1" ORDER BY "s1"."t1"."f1" ASC',
    # 'SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" INNER JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC',
]

multi_table = [
    'SELECT f1,f2 FROM t1 INNER JOIN t2 ON f1=f2 ORDER BY f1',
    'SELECT "f1","f2" FROM "t1" INNER JOIN "t2" ON "f1"="f2" ORDER BY "f1" ASC',
    'SELECT "s1"."f1","f2" FROM "t1" INNER JOIN "t2" ON "f1"="f2" ORDER BY "f1" ASC',

    'SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" INNER JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC',
    'SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" RIGHT JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC',
    'SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" LEFT JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC',
    'SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" RIGHT OUTER JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC',
    'SELECT "s1"."t1"."f1", "t2"."f2" FROM "t1" LEFT OUTER JOIN "t2" ON "f1"="f2" ORDER BY "t1"."f1" ASC',
]

ordered_table = [
    'SELECT * FROM t1 ORDER BY f1,f2',
    'SELECT * FROM t1 ORDER BY f1,f2 DESC',
]

@pytest.mark.parametrize('sql', one_table)
def test_single_table(sql):
    p = Parser(sql)
    assert p.unknown == []
    assert p.fields == ["f1"]
    assert p.tables == ["t1"]


@pytest.mark.parametrize('sql', multi_table)
def test_join(sql):
    p = Parser(sql)
    assert p.unknown == []
    assert p.fields == ["f1", "f2"]
    assert p.tables == ["t1", "t2"]



@pytest.mark.parametrize('sql', ordered_table)
def test_order(sql):
    p = Parser(sql)
    assert p.unknown == []
    assert p.order == ["f1", "f2"]



# @pytest.mark.parametrize('clause', ["SELECT", "SELECT DISTINCT"])
# @pytest.mark.parametrize('field', ['f1', '"f1"', 't1.f1', '"t1"."f1"', '"s1"."t1"."f1"'])
# def test_order(clause, field):
#     p = Parser(f"{clause} {field} FROM t1")
#     assert p.unknown == []
#     assert p.fields_name == ["f1"]
#     assert p.tables == ["t1"]


# @pytest.mark.parametrize('clause', ["SELECT", "SELECT DISTINCT"])
# def test_select_with_tablename(clause):
#     p = Parser(f"{clause} t1.f1 FROM t1")
#     assert p.unknown == []
#     assert p.fields == ["t1.f1"]
#     assert p.tables == ["t1"]

# def test_1():
#     p = Parser("SELECT DISTINCT f1 FROM t1")
#     assert p.unknown == []
#     assert p.fields == ["f1"]
#     assert p.tables == ["t1"]


#
# def test_get_tables1():
#     sql = "SELECT * from table1"
#     assert get_tables(sql) == ['table1']
#

# def test_get_tables_join():
#     sql = "SELECT * from table1 left join table2 on a=b"
#     assert get_tables(sql) == ['table1', 'table2']
#
#
# def test_add_schema_to_tables():
#     sql = "SELECT * from table1"
#     assert add_schema(sql, 'schema1') == "SELECT * from schema1.table1"
