# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse


def test_change_form(django_app, admin_user):
    url = reverse("admin:etools_partnerspartnerorganization_changelist")
    res = django_app.get(url, user=admin_user,
                         extra_environ={'HTTP_X_SCHEMA': "bolivia,chad,lebanon"})
    # FIXME: remove me (print)
    print(111, res)
    # FIXME: remove me (res.showbrowser)
    # res.showbrowser()
    pytest.fail()
