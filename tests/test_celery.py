from etools_datamart.celery import app


def test_autodiscover():
    ret = app.tasks
    assert 'load_data_hact' in ret, ret.keys()
