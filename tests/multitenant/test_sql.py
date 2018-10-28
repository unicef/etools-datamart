# -*- coding: utf-8 -*-
import pytest

from etools_datamart.apps.multitenant.sql import Parser

one_table = [
    'SELECT "f1" FROM "t1" ORDER BY "o1" ASC',
    'SELECT DISTINCT "f1" FROM "t1" ORDER BY "o1" ASC',
    'SELECT DISTINCT "t1"."f1" FROM "t1" ORDER BY "o1" ASC',
    'SELECT DISTINCT "t1"."f1" FROM "t1" ORDER BY "t1"."f1" ASC',
    'SELECT DISTINCT "s1"."t1"."f1" FROM "s1"."t1" ORDER BY "t1"."f1" ASC',
    'SELECT DISTINCT "s1"."t1"."f1" FROM "t1" ORDER BY "s1"."t1"."f1" ASC',
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
    'SELECT DISTINCT * FROM t1 ORDER BY f1,f2',
    'SELECT * FROM t1 ORDER BY f1,f2 DESC',
]

filtered_table = [

]


@pytest.mark.parametrize('sql', one_table)
def test_single_table(sql):
    p = Parser(sql)
    # assert p.unknown == []
    # assert p.fields == ["f1"]
    assert p.tables == ['"t1"']


def test_simple():
    p = Parser('SELECT id FROM "s1"."t1"')
    assert p.tables == ['"t1"']


def test_star():
    p = Parser('SELECT * FROM "s1"."t1" ORDER BY "t1"."f1"')
    assert p.tables == ['"t1"']


@pytest.mark.parametrize('sql', ordered_table)
def test_order(sql):
    p = Parser(sql)
    p.parse()
    assert p.parts['from'] == ' FROM t1'


def test_where1():
    p = Parser('SELECT "f1" FROM t1 WHERE f1=1 AND f2=2')
    p.parse()
    assert p.where == "WHERE f1=1 AND f2=2"


def test_where2():
    p = Parser('SELECT "f1" FROM t1 WHERE f1=%s')
    p.parse()
    assert p.where == "WHERE f1=%s"


@pytest.mark.parametrize('sql', ordered_table)
def test_split(sql):
    p = Parser(sql)
    assert p.join(p.split(sql)) == sql


def test_add_schema1():
    sql = 'SELECT "f1" AS "f1" FROM "t1"'
    p = Parser(sql)
    assert p.set_schema("bolivia") == 'SELECT "f1" AS "f1", \'bolivia\' AS __schema FROM "bolivia"."t1"'


def test_count_multitenant():
    p = Parser('SELECT COUNT(*) FROM "t1"')
    assert p.with_schemas("b",
                          "c") == 'SELECT COUNT(id) FROM ' \
                                  '(SELECT id, \'b\' AS __schema FROM "b"."t1" ' \
                                  'UNION ALL ' \
                                  'SELECT id, \'c\' AS __schema FROM "c"."t1") as __count'


def test_select_multitenant():
    p = Parser('SELECT * FROM "t1"')
    assert p.with_schemas("b",
                          "c") == 'SELECT * FROM (SELECT *, \'b\' AS __schema FROM "b"."t1" UNION ALL SELECT *, \'c\' AS __schema FROM "c"."t1") as __query'


def test_select_with_order_multitenant():
    p = Parser('SELECT * FROM "t1" ORDER BY "f1"')
    assert p.with_schemas("b",
                          "c") == 'SELECT * FROM ' \
                                  '(SELECT *, \'b\' AS __schema FROM "b"."t1" ' \
                                  'UNION ALL ' \
                                  'SELECT *, \'c\' AS __schema FROM "c"."t1") as __query ORDER BY f1'
