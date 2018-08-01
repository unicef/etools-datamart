# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from etools_datamart.libs.wallet import Wallet

wallet_filename = Path(__file__).parent / 'wallet.json'
global_filename = Path(__file__).parent / 'global.json'
obfuscated_filename = Path(__file__).parent / 'obfuscated.json'


@pytest.fixture
def credentials():
    f1 = Path(__file__).parent / '~aaaa.json'
    with f1.open('wb') as f:
        f.write(open(wallet_filename).read().encode('utf8'))
    yield str(f1)
    # f1.unlink()


def test_wallet_base():
    w = Wallet(wallet_filename, obfuscate=False)
    assert w.db.username == 'username1'
    assert w.db.password == 'password1'


def test_merge(monkeypatch):
    monkeypatch.setattr('etools_datamart.libs.wallet.GLOBAL_CREDENTIALS',
                        global_filename)
    w = Wallet(wallet_filename, obfuscate=False)
    assert w.db.username == 'username1'
    assert w.db.password == 'password1'

    assert w.system.username == 'username1'
    assert w.system.password == 'password1'


def test_no_global(monkeypatch):
    monkeypatch.setattr('etools_datamart.libs.wallet.GLOBAL_CREDENTIALS', '')
    w = Wallet(wallet_filename, obfuscate=False)
    assert w.db.username == 'username1'
    assert w.db.password == 'password1'


def test_obfuscate(monkeypatch, credentials):
    monkeypatch.setattr('etools_datamart.libs.wallet.GLOBAL_CREDENTIALS',
                        credentials)
    w = Wallet(credentials)
    assert w.db.username == 'username1'
    assert w.db.password == 'password1'


def test_obfuscated(monkeypatch):
    monkeypatch.setattr('etools_datamart.libs.wallet.GLOBAL_CREDENTIALS',
                        obfuscated_filename)

    w = Wallet(obfuscated_filename, obfuscate=False)
    assert w.db.username == 'username1'
    assert w.db.password == 'password1'


def test_access_by_key(monkeypatch):
    monkeypatch.setattr('etools_datamart.libs.wallet.GLOBAL_CREDENTIALS',
                        global_filename)
    w = Wallet(wallet_filename, obfuscate=False)

    assert w['global']['password'] == 'password1'


def test_keyerror():
    w = Wallet(wallet_filename, obfuscate=False)
    with pytest.raises(AttributeError):
        assert w['--']


def test_attributeerror():
    w = Wallet(wallet_filename, obfuscate=False)
    with pytest.raises(AttributeError):
        assert w.wrong

    with pytest.raises(AttributeError):
        assert w.db.wrong


def test_silent():
    w = Wallet(wallet_filename, obfuscate=False, silent=True)
    assert w.wrong is None
    assert w.db.wrong is None
