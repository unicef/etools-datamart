# -*- coding: utf-8 -*-
from django.db import connections
from django.urls import reverse

from etools_datamart.apps.etools.models import PartnersPartnerorganization
from etools_datamart.state import state


def test_changelist(django_app, admin_user):
    url = reverse('admin:login')
    res = django_app.get(url)
    res.form['username'] = 'admin'
    res.form['password'] = 'password'
    res = res.form.submit()
    res = res.follow().follow()

    url = reverse("admin:etools_partnerspartnerorganization_changelist")
    res = django_app.get(url,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon"})
    assert res.status_code == 200


def test_change_form(django_app, admin_user):
    # conn = connections['etools']
    # conn.clear_search_paths()
    schemas = ['bolivia', 'chad']
    state.schemas = schemas

    obj = PartnersPartnerorganization.objects.first()
    url = reverse('admin:login')
    res = django_app.get(url)
    res.form['username'] = 'admin'
    res.form['password'] = 'password'
    res = res.form.submit()
    res = res.follow().follow()

    url = reverse("admin:etools_partnerspartnerorganization_change", args=[f"{obj.pk}-bolivia"])
    res = django_app.get(url,
                         extra_environ={'HTTP_X_SCHEMA': ",".join(schemas)})
    assert res.status_code == 200
    assert res.context['original'].pk == obj.pk
    res = res.form.submit()
    assert res.status_code == 302


def test_select_schema(django_app, admin_user):
    url = reverse('admin:login')
    res = django_app.get(url)
    res.form['username'] = 'admin'
    res.form['password'] = 'password'
    res = res.form.submit()
    res = res.follow().follow()

    url = reverse("multitenant:select-schema")
    res = django_app.get(url, extra_environ={'HTTP_X_SCHEMA': ""})
    res = res.form.submit()
    assert res.status_code == 200

    res.form['bolivia'] = True
    res = res.form.submit()
    assert res.status_code == 302

