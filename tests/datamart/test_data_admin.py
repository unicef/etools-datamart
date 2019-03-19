# -*- coding: utf-8 -*-
from unittest.mock import MagicMock

from django.contrib import messages
from django.contrib.admin.sites import site
from django.urls import reverse

import pytest
from strategy_field.utils import fqn
from test_utilities.factories import factories_registry


def pytest_generate_tests(metafunc):
    if 'modeladmin' in metafunc.fixturenames:
        m = []
        ids = []
        for model, admin in site._registry.items():
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


#
# @pytest.mark.django_db()
# def test_pmpindicators_list(django_app, admin_user):
#     url = reverse("admin:data_pmpindicators_changelist")
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200


@pytest.mark.django_db()
def test_pmpindicators_filter(django_app, admin_user):
    url = reverse("admin:data_pmpindicators_changelist")
    url = f"{url}?country_name=bolivia,chad,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


# @pytest.mark.django_db()
# def test_pmpindicators_detail(django_app, staff_user, settings):
#     i = PMPIndicatorFactory()
#     url = reverse("admin:data_pmpindicators_change", args=[i.pk])
#     assert staff_user.is_authenticated
#     with user_grant_permissions(staff_user, ['data.change_pmpindicators']):
#         res = django_app.get(url, user=staff_user)
#         assert res.status_code == 200
#         res = res.form.submit().follow()
#         assert res.status_code == 200
#         storage = res.context['messages']
#         assert [m.message for m in storage] == ['This admin is read-only. Record not saved.']


# @pytest.mark.django_db()
# def test_pmpindicators_detail_supersuser(django_app, admin_user, settings):
#     i = PMPIndicatorFactory()
#     url = reverse("admin:data_pmpindicators_change", args=[i.pk])
#     assert admin_user.is_authenticated
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     res = res.form.submit()
#     assert res.status_code == 302, f"Submit failed with: {repr(res.context['adminform'].errors)}"


# def test_pmpindicators_refresh(django_app, admin_user):
#     url = reverse("admin:data_pmpindicators_changelist")
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     res = res.click("Refresh").follow()
#     assert res.status_code == 200
#     storage = res.context['messages']
#     assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]


# def test_pmpindicators_invalidate_cache(django_app, admin_user, service):
#     url = reverse("admin:data_pmpindicators_invalidate_cache")
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 302
#
#
# def test_pmpindicators_api(django_app, admin_user, service):
#     url = reverse("admin:data_pmpindicators_api")
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 302
#
#
# def test_pmpindicators_truncate(django_app, admin_user):
#     url = reverse("admin:data_pmpindicators_changelist")
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     res = res.click("Truncate")
#     assert res.status_code == 200
#     res = res.form.submit().follow()
#     assert res.status_code == 200
#     storage = res.context['messages']
#     assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]
#
#
# def test_pmpindicators_queue(django_app, admin_user):
#     url = reverse("admin:data_pmpindicators_changelist")
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     res = res.click("Queue").follow()
#     assert res.status_code == 200
#     storage = res.context['messages']
#     assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ['success'], [m.message for m in storage]
#
#
# def test_pmpindicators_filterimng(django_app, admin_user):
#     url = reverse("admin:data_pmpindicators_changelist")
#     res = django_app.get(f"{url}", user=admin_user)
#     assert res.status_code == 200
#
