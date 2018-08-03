# -*- coding: utf-8 -*-
from django.urls import reverse


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
