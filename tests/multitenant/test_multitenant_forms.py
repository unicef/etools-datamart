import pytest

from etools_datamart.apps.multitenant.views import SelectSchema


@pytest.mark.parametrize("new_params,remove,expected",
                         ([None, None, "?a=1&b=2"],
                          [{"a": "22"}, None, "?a=22&b=2"],
                          [None, ["b"], "?a=1"],
                          [{"c": "33"}, None, "?a=1&b=2&c=33"],
                          [{"b": None}, None, "?a=1"],
                          [{"c": None}, None, "?a=1&b=2"],
                          ))
def test_form(new_params, remove, expected):
    form = SelectSchema()
    form.params = {'a': "1", "b": "2"}
    assert form.get_query_string(new_params, remove) == expected
