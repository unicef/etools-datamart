# -*- coding: utf-8 -*-
import pytest

from etools_datamart.state import state
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


def test_query_public(db):
    state.schemas = ['bolivia']
    assert AuthGroup.objects.all()


def test_query_single_tenant(db):
    state.schemas = ['bolivia']
    assert len(PartnersPartnerorganization.objects.all()) == 190


def test_query_multi_tenant(db):
    state.schemas = ['bolivia', 'chad']
    assert len(PartnersPartnerorganization.objects.all()) == 622


def test_count_single_tenant(db):
    state.schemas = ['bolivia']
    assert PartnersPartnerorganization.objects.count() == 190


def test_count_multi_tenant1(db):
    state.schemas = ['bolivia', 'chad']
    assert PartnersPartnerorganization.objects.count() == 622


def test_count_multi_tenant2(db):
    state.schemas = ['bolivia', 'chad']
    assert PartnersPartnerorganization.objects.count() == 622
