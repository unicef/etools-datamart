import json
from pathlib import Path

import pytest

from etools_datamart.api.urls import urlpatterns

CONTRACT_FILE = Path(__file__).parent / 'test_urls.json'


def name(func):
    if func is None:
        return ""
    else:
        return "%s.%s" % (func.__module__, func.__name__)


def list_urls(urllist, depth=0, urls=None):
    _urls = urls or list()
    for entry in urllist:
        _urls.append(entry.pattern.regex.pattern)

        if hasattr(entry, 'url_patterns'):
            list_urls(entry.url_patterns, depth + 1, _urls)

    return _urls


def get_urls(data_file):
    if not data_file.exists():
        current_urls = list_urls(urlpatterns)
        data_file.write_text(json.dumps(current_urls))

    return json.loads(data_file.read_text())


def pytest_generate_tests(metafunc):
    # if metafunc.config.option.record_new_urls:
    #     CONTRACT_FILE.delete()

    if 'current_url' in metafunc.fixturenames:
        current = list_urls(urlpatterns)
        metafunc.parametrize("current_url", current)
    elif 'contract_url' in metafunc.fixturenames:
        contract = get_urls(CONTRACT_FILE)
        metafunc.parametrize("contract_url", contract)


@pytest.fixture(scope='module')
def contract(request):
    yield get_urls(CONTRACT_FILE)
    if request.config.option.record_new_urls:
        if ADDED:
            if MISSING:
                pass
            else:
                CONTRACT_FILE.rename(CONTRACT_FILE.with_suffix('.bak'))


CREATE_CONTRACT_FILE = False
MISSING = False
ADDED = False


@pytest.fixture(scope='module')
def current():
    return list_urls(urlpatterns)


def test_addedd(request, contract, current_url):
    global ADDED
    if current_url not in contract:
        if request.config.option.record_new_urls:
            ADDED = True
            pytest.fail("API ADDED: '%s' is a new url and contract file '%s' must be recreated" % (current_url,
                                                                                                   CONTRACT_FILE))
        else:
            pytest.fail("API ADDED: '%s' is a new url and contract file '%s' must be recreated" % (current_url,
                                                                                                   CONTRACT_FILE))


def test_missing(current, contract_url):
    global MISSING
    if contract_url not in current:
        MISSING = True
        pytest.fail("API REMOVED: '%s' endpoint has been removed" % contract_url)

# def test_urls():
#     contract_file = Path(__file__).parent / 'test_urls.json'
#     contract = get_urls(contract_file)
#     current = list_urls(urlpatterns)
#     # check all previous urls are preserved
#     for url in contract:
#         if url not in current:
#             pytest.fail("API REMOVED: '%s' endpoint has been removed" % url)
#
#     # check for any added urls
#     for url in current:
#         if url not in contract:
#             pytest.fail("API ADDED: '%s' is a new url and contract file '%s' must be recreated" % (url, contract_file))
#
#     # for url in list_urls(urlpatterns):
#     #     assert url in contract
#     #
