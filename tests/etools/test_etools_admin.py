# -*- coding: utf-8 -*-
import pytest
from django.contrib.admin.sites import site
from django.db import connections
from django.urls import reverse

from etools_datamart.apps.etools.models import PartnersPartnerorganization
from etools_datamart.apps.multitenant.models import TenantModel

conn = connections['etools']


def pytest_generate_tests(metafunc):
    if 'modeladmin' in metafunc.fixturenames:
        m = []
        ids = []
        for model, admin in site._registry.items():
            if model._meta.app_label == 'etools':
                m.append(admin)
                ids.append(admin.__class__.__name__)

        metafunc.parametrize("modeladmin", m, ids=ids)


def test_changelist(django_app, admin_user, modeladmin):
    opts = modeladmin.model._meta
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_change(django_app, admin_user, modeladmin):
    opts = modeladmin.model._meta
    conn.set_schemas(["bolivia"])
    obj = modeladmin.model.objects.first()
    if not obj:
        pytest.skip("No object found")
    if issubclass(modeladmin.model, TenantModel):
        key = f"{obj.pk}-bolivia"
    else:
        key = obj.pk
    url = reverse(f"admin:{opts.app_label}_{opts.model_name}_change",
                  args=[key])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200, url


def test_changelist_all(django_app, admin_user):
    url = reverse("admin:etools_partnerspartnerorganization_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    # schemaes = res.context['schemas']
    # qs = res.context['queryset']


def test_changelist_many(django_app, admin_user):
    url = reverse("admin:etools_partnerspartnerorganization_changelist")
    url = f"{url}?country_name=bolivia,chad,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_changelist_single(django_app, admin_user):
    url = reverse("admin:etools_partnerspartnerorganization_changelist")
    url = f"{url}?country_name=bolivia"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_change_form(django_app, admin_user):
    schemas = ['bolivia', 'chad']
    conn.set_schemas(schemas)
    obj = PartnersPartnerorganization.objects.first()
    assert obj

    url = reverse("admin:etools_partnerspartnerorganization_change", args=[f"{obj.pk}-bolivia"])
    url = f"{url}?country_name=bolivia,chad"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    assert res.context['original'].pk == obj.pk
    res = res.form.submit()
    assert res.status_code == 302


def test_select_schema(django_app, admin_user):
    url = reverse("select-schema")
    res = django_app.get(url, user=admin_user)
    res = res.form.submit()
    assert res.status_code == 200

    res.form['bolivia'] = True
    res = res.form.submit()
    assert res.status_code == 302


def test_changelist2(django_app, admin_user):
    url = reverse("admin:etools_partnersagreement_changelist")
    url = f"{url}?country_name=bolivia,chad,lebanon"
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
