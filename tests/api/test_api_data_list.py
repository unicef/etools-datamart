import pytest

from etools_datamart.api.urls import router

FORMATS = (
    ('', 'application/json'),
    ('csv', 'text/csv; charset=utf-8'),
    ('iqy', 'text/plain; charset=utf-8'),
    ('json', 'application/json'),
    ('ms-json', 'application/json'),
    ('ms-xml', 'application/xml; charset=utf-8'),
    ('pdf', 'application/pdf; charset=utf-8'),
    ('txt', 'text/plain; charset=utf-8'),
    ('xhtml', 'text/html; charset=utf-8'),
    ('xlsx', 'application/xlsx; charset=utf-8'),
    ('xml', 'application/xml; charset=utf-8'),
)


def pytest_generate_tests(metafunc, *args):
    if 'serializer' in metafunc.fixturenames:
        params = []
        ids = []
        for prefix, viewset, basenametry in router.registry:
            if prefix.startswith('datamart/rapidpro'):
                pass
            elif prefix.startswith('datamart/'):
                sers = viewset.serializers_fieldsets.keys()
                for ser in sers:
                    params.append([viewset, ser])
                    ids.append(f'{viewset.__name__}-{ser}')
        metafunc.parametrize("viewset,serializer", params, ids=ids)


@pytest.mark.parametrize("format,ct", FORMATS, ids=[f[0] for f in FORMATS])
def test_list(client, viewset, format, ct, data, serializer):
    res = client.get(f"{viewset.get_service().endpoint}?format={format}")
    assert res.status_code == 200, res
    assert res.content
    assert res['Content-Type'] == ct
