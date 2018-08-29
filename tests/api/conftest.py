# -*- coding: utf-8 -*-
import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    assert client.login(username='admin', password='password')
    return client
