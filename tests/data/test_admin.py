# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse
from django_webtest import WebTestMixin

from test_utils.factories import PMPIndicatorFactory


class MixinWithInstanceVariables(WebTestMixin):
    """
    Override WebTestMixin to make all of its variables instance variables
    not class variables; otherwise multiple django_app_factory fixtures contend
    for the same class variables
    """

    def __init__(self):
        self.extra_environ = {}
        self.csrf_checks = True
        self.setup_auth = True


@pytest.fixture(scope='session')
def django_app_mixin():
    app_mixin = MixinWithInstanceVariables()
    return app_mixin


@pytest.fixture
def django_app(django_app_mixin):
    django_app_mixin._patch_settings()
    django_app_mixin.renew_app()
    yield django_app_mixin.app
    django_app_mixin._unpatch_settings()


@pytest.mark.django_db(transaction=True)
def test_pmpindicators_list(django_app, admin_user):
    url = reverse('admin:login')
    res = django_app.get(url)
    res.form['username'] = 'admin'
    res.form['password'] = 'password'
    res = res.form.submit()
    res = res.follow().follow()

    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon"})
    assert res.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_pmpindicators_detail(django_app, admin_user, settings):
    i = PMPIndicatorFactory()
    url = reverse('admin:login')
    res = django_app.get(url)
    res.form['username'] = 'admin'
    res.form['password'] = 'password'
    res = res.form.submit()
    res = res.follow().follow()
    url = reverse("admin:data_pmpindicators_change", args=[i.pk])
    assert admin_user.is_authenticated
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon"})
    assert res.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_pmpindicators_refresh(django_app, admin_user):
    url = reverse('admin:login')
    res = django_app.get(url)
    res.form['username'] = 'admin'
    res.form['password'] = 'password'
    res = res.form.submit()
    res = res.follow().follow()
    url = reverse("admin:data_pmpindicators_changelist")
    res = django_app.get(url,
                         user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon"})
    res = res.click('Refresh').follow()
    assert res.status_code == 200
