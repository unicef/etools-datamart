from pathlib import Path

import vcr
from unicef_security.azure import Synchronizer


def test_token():
    s = Synchronizer()
    assert s.access_token


@vcr.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/test_user_data.yml'))
def test_user_data():
    s = Synchronizer()
    assert s.get_user('sapostolico@unicef.org')
