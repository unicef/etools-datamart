# -*- coding: utf-8 -*-
import json

import pytest
from django.contrib.auth.models import User
from test_utilities.factories import APIRequestLogFactory


@pytest.fixture
def system_user(db):
    return User.objects.get(username='system')


@pytest.fixture
def log(db):
    return APIRequestLogFactory()


@pytest.fixture
def log_with_params(db):
    return APIRequestLogFactory(query_params=json.dumps({"a": 1}))
