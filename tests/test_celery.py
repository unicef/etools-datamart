from etools_datamart.celery import app


def test_autodiscover():
    ret = app.tasks
    assert 'etools_datamart.apps.etl.tasks.etl.load_hact' in ret
