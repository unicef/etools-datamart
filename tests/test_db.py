# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.db import connections
from django.urls import reverse

from etools_datamart.apps.etools.models import AuthGroup, PartnersPartnerorganization


#
# from django.db.backends.signals import connection_created
#
# def set_search_path(sender, **kwargs):
#     conn = kwargs.get('connection')
#     schema = "public"
#     if conn is not None:
#         cursor = conn.cursor()
#         cursor.execute(f"SET search_path={schema},bolivia")
#
# connection_created.connect(set_search_path)

def test_query(db):
    # Public
    assert AuthGroup.objects.all()

    conn = connections['etools']

    # conn.set_schema('bolivia')
    # assert PartnersPartnerorganization.objects.count() == 190

    conn.set_schema('bolivia,chad')
    assert PartnersPartnerorganization.objects.count() == 190
