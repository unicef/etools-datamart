from unicef_security.azure import Synchronizer


def test_token():
    s = Synchronizer()
    assert s.access_token


def test_user_data():
    s = Synchronizer()
    assert s.get_user('sapostolico@unicef.org')
