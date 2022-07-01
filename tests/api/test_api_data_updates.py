import pytest
from api.test_api_data_list import FORMATS, pytest_generate_tests


@pytest.mark.parametrize("format,ct", FORMATS, ids=[f[0] for f in FORMATS])
def test_updates(client, viewset, format, ct, data, serializer):
    res = client.get(f"{viewset.get_service().endpoint}updates/?format={format}")
    assert res.status_code == 200, res
    assert res.content
    assert res['Content-Type'] == ct
