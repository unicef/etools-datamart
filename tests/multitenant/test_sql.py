# -*- coding: utf-8 -*-
import re

import pytest
import sqlparse
from django.db import connections

from etools_datamart.apps.multitenant.admin import format_stm
from etools_datamart.apps.multitenant.postgresql.utils import raw_sql
from etools_datamart.apps.multitenant.sql import Parser
from etools_datamart.state import state

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
                          "c") == 'SELECT COUNT(id) FROM (SELECT id, \'b\' AS __schema FROM "b"."t1" UNION ALL SELECT id, \'c\' AS __schema FROM "c"."t1") as __count'


def test_select_multitenant():
    p = Parser('SELECT * FROM "t1"')
    assert p.with_schemas("b",
                          "c") == 'SELECT * FROM (SELECT *, \'b\' AS __schema FROM "b"."t1" UNION ALL SELECT *, \'c\' AS __schema FROM "c"."t1") as __query'


def test_select_with_order_multitenant():
    p = Parser('SELECT * FROM "t1" ORDER BY "f1"')
    assert p.with_schemas("b",
                          "c") == 'SELECT * FROM (SELECT *, \'b\' AS __schema FROM "b"."t1" UNION ALL SELECT *, \'c\' AS __schema FROM "c"."t1") as __query ORDER BY f1'


def test_complex(db):
    _in = '''SELECT "partners_intervention"."id", "partners_intervention"."__schema", "partners_intervention"."created",
       "partners_intervention"."modified", "partners_intervention"."document_type", "partners_intervention"."number",
       "partners_intervention"."title", "partners_intervention"."status", "partners_intervention"."start",
       "partners_intervention"."end", "partners_intervention"."submission_date",
       "partners_intervention"."submission_date_prc", "partners_intervention"."review_date_prc",
       "partners_intervention"."prc_review_document", "partners_intervention"."signed_by_unicef_date",
       "partners_intervention"."signed_by_partner_date", "partners_intervention"."population_focus",
       "partners_intervention"."agreement_id", "partners_intervention"."partner_authorized_officer_signatory_id",
       "partners_intervention"."unicef_signatory_id", "partners_intervention"."signed_pd_document",
       "partners_intervention"."country_programme_id", "partners_intervention"."contingency_pd",
       "partners_intervention"."metadata", "partners_intervention"."in_amendment",
       MAX("funds_fundsreservationheader"."end_date") AS "frs__end_date__max",
       MIN("funds_fundsreservationheader"."start_date") AS "frs__start_date__min",
       SUM("funds_fundsreservationheader"."total_amt_local") AS "frs__total_amt_local__sum",
       SUM("funds_fundsreservationheader"."outstanding_amt_local") AS "frs__outstanding_amt_local__sum",
       SUM("funds_fundsreservationheader"."actual_amt_local") AS "frs__actual_amt_local__sum",
       SUM("funds_fundsreservationheader"."intervention_amt") AS "frs__intervention_amt__sum",
       COUNT(DISTINCT "funds_fundsreservationheader"."currency") AS "frs__currency__count", MAX("funds_fundsreservationheader"."currency") AS "max_fr_currency",
       COUNT(CASE
                 WHEN "funds_fundsreservationheader"."multi_curr_flag" = TRUE THEN 1
                 ELSE NULL
             END) AS "multi_curr_flag"
FROM "partners_intervention"
LEFT OUTER JOIN "funds_fundsreservationheader" ON ("partners_intervention"."id" = "funds_fundsreservationheader"."intervention_id")
GROUP BY "partners_intervention"."id", "partners_intervention"."__schema", "partners_intervention"."created",
         "partners_intervention"."modified", "partners_intervention"."document_type",
         "partners_intervention"."number", "partners_intervention"."title", "partners_intervention"."status",
         "partners_intervention"."start", "partners_intervention"."end",
         "partners_intervention"."submission_date", "partners_intervention"."submission_date_prc",
         "partners_intervention"."review_date_prc", "partners_intervention"."prc_review_document",
         "partners_intervention"."signed_by_unicef_date", "partners_intervention"."signed_by_partner_date",
         "partners_intervention"."population_focus", "partners_intervention"."agreement_id",
         "partners_intervention"."partner_authorized_officer_signatory_id", "partners_intervention"."unicef_signatory_id",
         "partners_intervention"."signed_pd_document", "partners_intervention"."country_programme_id",
         "partners_intervention"."contingency_pd", "partners_intervention"."metadata",
         "partners_intervention"."in_amendment"'''

    _expected = '''SELECT "partners_intervention"."id", 'indonesia' AS __schema, "partners_intervention"."created",
       "partners_intervention"."modified", "partners_intervention"."document_type", "partners_intervention"."number",
       "partners_intervention"."title", "partners_intervention"."status", "partners_intervention"."start",
       "partners_intervention"."end", "partners_intervention"."submission_date",
       "partners_intervention"."submission_date_prc", "partners_intervention"."review_date_prc",
       "partners_intervention"."prc_review_document", "partners_intervention"."signed_by_unicef_date",
       "partners_intervention"."signed_by_partner_date", "partners_intervention"."population_focus",
       "partners_intervention"."agreement_id", "partners_intervention"."partner_authorized_officer_signatory_id",
       "partners_intervention"."unicef_signatory_id", "partners_intervention"."signed_pd_document",
       "partners_intervention"."country_programme_id", "partners_intervention"."contingency_pd",
       "partners_intervention"."metadata", "partners_intervention"."in_amendment",
       MAX("funds_fundsreservationheader"."end_date") AS "frs__end_date__max",
       MIN("funds_fundsreservationheader"."start_date") AS "frs__start_date__min",
       SUM("funds_fundsreservationheader"."total_amt_local") AS "frs__total_amt_local__sum",
       SUM("funds_fundsreservationheader"."outstanding_amt_local") AS "frs__outstanding_amt_local__sum",
       SUM("funds_fundsreservationheader"."actual_amt_local") AS "frs__actual_amt_local__sum",
       SUM("funds_fundsreservationheader"."intervention_amt") AS "frs__intervention_amt__sum",
       COUNT(DISTINCT "funds_fundsreservationheader"."currency") AS "frs__currency__count", MAX("funds_fundsreservationheader"."currency") AS "max_fr_currency",
       COUNT(CASE
                 WHEN "funds_fundsreservationheader"."multi_curr_flag" = TRUE THEN 1
                 ELSE NULL
             END) AS "multi_curr_flag"
FROM "indonesia"."partners_intervention"
LEFT OUTER JOIN "indonesia"."funds_fundsreservationheader" ON ("indonesia"."partners_intervention"."id" = "indonesia"."funds_fundsreservationheader"."intervention_id")
GROUP BY "partners_intervention"."id", "partners_intervention"."created", 
         "partners_intervention"."modified", "partners_intervention"."document_type", 
         "partners_intervention"."number", "partners_intervention"."title", "partners_intervention"."status",
         "partners_intervention"."start", "partners_intervention"."end",
         "partners_intervention"."submission_date", "partners_intervention"."submission_date_prc",
         "partners_intervention"."review_date_prc", "partners_intervention"."prc_review_document",
         "partners_intervention"."signed_by_unicef_date", "partners_intervention"."signed_by_partner_date",
         "partners_intervention"."population_focus", "partners_intervention"."agreement_id",
         "partners_intervention"."partner_authorized_officer_signatory_id", "partners_intervention"."unicef_signatory_id",
         "partners_intervention"."signed_pd_document", "partners_intervention"."country_programme_id",
         "partners_intervention"."contingency_pd", "partners_intervention"."metadata",
         "partners_intervention"."in_amendment"'''

    # first we check that _expected is a valid sql statement
    conn = connections['etools']
    state.schemas = ["indonesia"]
    cur = conn.cursor()
    cur.execute(raw_sql(_expected))
    row = cur.fetchone()
    assert len(row) == 34
    # now the rela test

    p = Parser(_in)
    assert format_stm(p.with_schemas("indonesia")) == format_stm(_expected)
