from unittest.mock import MagicMock

from django.contrib import messages
from django.contrib.admin.sites import site
from django.urls import reverse

import pytest
from strategy_field.utils import fqn
from test_utilities.factories import factories_registry

EXCLUDED_MODELS = [
    'GeoName',
]


def pytest_generate_tests(metafunc):
    if 'modeladmin' in metafunc.fixturenames:
        m = []
        ids = []
        for model, admin in site._registry.items():
            if model.__name__ not in EXCLUDED_MODELS:
                if model._meta.app_label == 'data':
                    m.append(admin)
                    ids.append(admin.__class__.__name__)
        metafunc.parametrize("modeladmin", m, ids=ids)


@pytest.fixture()
def data(db, request):
    # TIPS: database access is forbidden in pytest_generate_tests
    modeladmin = request.getfixturevalue('modeladmin')
    factory = factories_registry[modeladmin.model]
    return (factory(schema_name='bolivia'),
            factory(schema_name='chad'),
            factory(schema_name='lebanon'))


def test_changelist(django_app, admin_user, modeladmin):
    opts = modeladmin.model._meta
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_change(django_app, admin_user, modeladmin):
    opts = modeladmin.model._meta
    factory = factories_registry[modeladmin.model]
    obj = factory()
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_change",
                  args=[obj.pk])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200, url


def test_refresh(django_app, admin_user, modeladmin, monkeypatch):
    target = fqn(modeladmin.model)
    monkeypatch.setattr(f'{target}.loader.load', MagicMock())
    opts = modeladmin.model._meta
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")

    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Refresh").follow()
    assert res.status_code == 200
    storage = res.context['messages']
    assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]


def test_api(django_app, admin_user, modeladmin):
    opts = modeladmin.model._meta
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
    res = django_app.get(url, user=admin_user)
    res = res.click("Api").follow()
    assert res.status_code == 200


def test_queue(django_app, admin_user, modeladmin, monkeypatch):
    opts = modeladmin.model._meta
    target = fqn(modeladmin.model)
    monkeypatch.setattr(f'{target}.loader.task.delay', MagicMock())

    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
    res = django_app.get(url, user=admin_user)
    res = res.click("Queue").follow()
    assert res.status_code == 200


def test_invalidate_cache(django_app, admin_user, modeladmin):
    opts = modeladmin.model._meta
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
    res = django_app.get(url, user=admin_user)
    res = res.click("Invalidate Cache").follow()
    assert res.status_code == 200


def test_filter(django_app, admin_user, modeladmin, data):
    opts = modeladmin.model._meta
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
    url = f"{url}?country_name=bolivia,chad,lebanon"

    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200, url


@pytest.mark.django_db()
def test_data_index(django_app, admin_user):
    url = reverse("admin:app_list", args=['data'])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


@pytest.mark.django_db()
def test_pmpindicators_filter(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    url = f"{url}?country_name=bolivia,chad,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
