from etools_datamart.apps.data.loader import EtlResult
from etools_datamart.apps.etl.results import etl_decoder, etl_dumps, etl_loads, EtlEncoder

# def test_result_eq():
#     assert EtlResult() == EtlResult()


# def test_result_ne():
#     assert not EtlResult() == EtlResult(created=1)


# def test_result_eq_dict():
#     assert EtlResult() == {'created': 0, 'updated': 0, 'unchanged': 0, 'deleted': 0}


# def test_result_ne_dict():
#     assert not EtlResult() == {'created': 1, 'updated': 1, 'unchanged': 1, 'deleted': 0}


# def test_result_ne_other():
#     assert not EtlResult() == 1


def test_encoder():
    e = EtlEncoder()
    assert e.encode(
        EtlResult(1, 1, 1)) == '{"__type__": "__EtlResult__", ' \
                               '"data": {"created": 1, "updated": 1, "unchanged": 1, "deleted": 0, "status": "SUCCESS", "error": null}}'


def test_encoder2():
    e = EtlEncoder()
    assert e.encode({"a": float(1.1)}) == '{"a": 1.1}'
    assert e.default({"a": float(1.1)}) == {"a": 1.1}


def test_decode():
    assert etl_decoder({}) == {}


def test_decode2():
    assert etl_decoder({"__type__": "__EtlResult__",
                        "data": {"created": 1,
                                 "updated": 1,
                                 "unchanged": 1,
                                 "deleted": 0,
                                 "status": "SUCCESS",
                                 "error": None}})


def test_dumps():
    assert etl_dumps(
        EtlResult(1, 1,
                  1)) == '{"__type__": "__EtlResult__", "data": {"created": 1, "updated": 1, "unchanged": 1, "deleted": 0, "status": "SUCCESS", "error": null}}'


def test_dumps2():
    assert etl_dumps({} == '{}')


def test_loads():
    assert etl_loads(etl_dumps({"a": 1})) == {"a": 1}
