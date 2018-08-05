# -*- coding: utf-8 -*-


def test_wsgi():
    from etools_datamart.config.wsgi import application
    assert application
