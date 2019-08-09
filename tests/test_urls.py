import collections
import json
import pickle
from pathlib import Path

import pytest

from etools_datamart.api.urls import urlpatterns


def name(func):
    if func is None:
        return ""
    else:
        return "%s.%s" % (func.__module__, func.__name__)


def list_urls(urllist, depth=0, urls=None):
    _urls = urls or list()
    for entry in urllist:
        _urls.append(entry.pattern.regex.pattern)
        # _urls.append("||".join([getattr(entry, "name", "-"),
        #                         entry.pattern.regex.pattern,
        #                         name(entry.callback)]))

        if hasattr(entry, 'url_patterns'):
            list_urls(entry.url_patterns, depth + 1, _urls)

    return _urls


def get_urls(data_file):
    if not data_file.exists():
        current_urls = list_urls(urlpatterns)
        data_file.write_text(json.dumps(current_urls))

    return json.loads(data_file.read_text())


@pytest.mark.django_db
def test_urls():
    contract_file = Path(__file__).parent / 'test_urls.json'
    contract = get_urls(contract_file)
    current = list_urls(urlpatterns)
    # check all previous urls are preserved
    for url in contract:
        if url not in current:
            pytest.fail("API REMOVED: '%s' endpoint has been removed" % url)

    # check for any added urls
    for url in current:
        if url not in contract:
            pytest.fail("API ADDED: '%s' is a new url and contract file '%s' must be recreated" % (url, contract_file))

    # for url in list_urls(urlpatterns):
    #     assert url in contract
    #
