from etools_datamart.apps.etl.results import etl_decoder, etl_dumps, etl_loads, EtlEncoder
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


def test_encoder():
    e = EtlEncoder()
    assert e.encode(
        EtlResult(1, 1, 1)) == '{"__type__": "__EtlResult__", "data": {"created": 1, "updated": 1, "unchanged": 1}}'


def test_encoder2():
    e = EtlEncoder()
    assert e.encode({}) == '{}'


def test_encode():
    assert etl_decoder({}) == {}


def test_dumps():
    assert etl_dumps(
        EtlResult(1, 1, 1)) == '{"__type__": "__EtlResult__", "data": {"created": 1, "updated": 1, "unchanged": 1}}'


def test_loads():
    assert etl_loads(etl_dumps({"a": 1})) == {"a": 1}
