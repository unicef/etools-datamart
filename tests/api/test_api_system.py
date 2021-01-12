from rest_framework.reverse import reverse

from etools_datamart.api.urls import router


def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        urls = filter(lambda url: 'system/' in url,
                      [reverse("api:%s" % url.name, args=['latest'])
                       for url in router.urls if url.name.endswith('-list')])
        metafunc.parametrize("url", urls)


def test_list(client, url):
    res = client.get(url, HTTP_X_SCHEMA="public")
    assert res.status_code == 200, res
    assert res.json()
