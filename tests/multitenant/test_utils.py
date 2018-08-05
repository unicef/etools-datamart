# -*- coding: utf-8 -*-
from etools_datamart.apps.multitenant.postgresql.utils import raw_sql, RawSql


def test_raw_sql():
    target = "SELECT * FROM table"
    q = raw_sql(target)
    assert isinstance(q, RawSql)

    assert isinstance(RawSql("") + q, RawSql)
    assert isinstance(raw_sql(1), RawSql)

    assert not isinstance("" + q, RawSql)
    assert not isinstance(q + "", RawSql)
    assert str(q) == target
