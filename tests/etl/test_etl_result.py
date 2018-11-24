from etools_datamart.apps.etl.tasks.etl import EtlResult


def test_result_eq():
    assert EtlResult() == EtlResult()


def test_result_ne():
    assert not EtlResult() == EtlResult(created=1)


def test_result_eq_dict():
    assert EtlResult() == {'created': 0, 'updated': 0, 'unchanged': 0}


def test_result_ne_dict():
    assert not EtlResult() == {'created': 1, 'updated': 1, 'unchanged': 1}


def test_result_ne_other():
    assert not EtlResult() == 1
