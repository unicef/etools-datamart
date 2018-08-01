# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import base64
import json
import logging
import os

import six

logger = logging.getLogger(__name__)

OBFUSCATE = ['password', 'pwd', 'token']
PREFIX = 'md5$'
GLOBAL_CREDENTIALS = os.environ.get('GLOBAL_CREDENTIALS',
                                    os.path.expanduser('~/.credentials.json'))

RESERVED = ['global', ]


def encrypt(plain):
    return '{}{}'.format(PREFIX, base64.b64encode(six.b(plain)).decode('ascii'))


def decrypt(encoded):
    return base64.b64decode(encoded[len(PREFIX):]).decode('utf-8')


CRYPTO = {
    'md5': (encrypt, decrypt)
}


def is_encrypted(value):
    return value.startswith(str(PREFIX))


class DictWrapper(dict):

    def __init__(self, *args, **kwargs) -> None:
        self.__dict__['_silent'] = kwargs.pop('__silent')
        self.__dict__['_decrypter'] = kwargs.pop('__decrypter')
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):
        try:
            v = self[item]
            if isinstance(v, dict):
                return DictWrapper(v,
                                   __decrypter=self._decrypter,
                                   __silent=self._silent)
            elif isinstance(v, six.string_types) and is_encrypted(v):
                return self._decrypter(v)
            else:
                return v
        except KeyError as e:
            if self._silent:
                return None
            raise AttributeError(e)


class Wallet(object):
    def __init__(self, filename, silent=False, obfuscate=True, crypter='md5'):
        self._filename = os.path.abspath(filename)
        self._silent = silent
        self._obfuscate = obfuscate
        self._crypter, self._decrypter = CRYPTO[crypter]
        self.__credentials = DictWrapper({},
                                         __decrypter=self._decrypter,
                                         __silent=self._silent)

        if os.path.exists(GLOBAL_CREDENTIALS):
            self._load(GLOBAL_CREDENTIALS)
        self._load(self._filename)

    def _load(self, filename):
        over = DictWrapper(json.load(open(str(filename))),
                           __decrypter=self._decrypter,
                           __silent=self._silent)
        data = self.__credentials.copy()
        data.update(over)
        self.__credentials = DictWrapper(data,
                                         __decrypter=self._decrypter,
                                         __silent=self._silent)

        if self._obfuscate:
            self._process(self._crypter, is_encrypted)

    def _process(self, func, test):
        def recurse(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    recurse(value)
                elif key.lower() in [item.lower() for item in OBFUSCATE] and not test(value):
                    d[key] = func(value)

        recurse(self.__credentials)
        json.dump(self.__credentials, open(self._filename, 'w'), indent=2)

    # def encrypt(self):
    #     self._process(encrypt, is_encrypted)

    def __getattr__(self, item):
        try:
            return getattr(self.__credentials, item)
        except (AttributeError, KeyError):
            raise AttributeError(f'Wallet does not have an entry for {item}')

    def __getitem__(self, item):
        try:
            return self.__credentials[item]
        except (AttributeError, KeyError):
            raise AttributeError(f'Wallet does not have an entry for {item}')
