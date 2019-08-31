# -*- coding: utf-8 -*-
from unittest.mock import Mock

from django.apps import apps
from django.db import connections


def pytest_generate_tests(metafunc):
    if 'context' in metafunc.fixturenames:
        config = apps.get_app_config('data')
        models = []
        ids = []
        for m in config.get_models():
            ctx = {'country': 1, 'year': 2019}
            models.append([m, ctx])
            ids.append(m.__name__)
        metafunc.parametrize("model,context", models, ids=ids)
    elif 'model' in metafunc.fixturenames:
        config = apps.get_app_config('data')
        metafunc.parametrize("model", config.get_models())


def test_model_str(model):
    assert str(model()) is not None


def test_model_loader(model):
    assert model().loader


def test_model_options(model):
    assert model().loader.config.source


def test_model_sync_deleted_records(model):
    assert model().loader.config.sync_deleted_records(Mock()) in [True, False]


def test_model_sync_get_queryset(db, model, context):
    connection = connections['etools']
    connection.set_schemas(['lebanon'])
    loader = model().loader
    loader.context = context
    assert loader.get_queryset().count() >= 0
