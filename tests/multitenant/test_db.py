# -*- coding: utf-8 -*-
import pytest
from django.db import connections

from etools_datamart.apps.etools.models import (ActionPointsActionpoint, AuthGroup,
                                                PartnersPartnerorganization, ReportsResult,)

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

RECORDS = 324  # Change this number each time etools dump is updated

conn = connections['etools']


def test_query_public(db):
    conn.set_schemas(['bolivia'])
    assert AuthGroup.objects.all()


def test_query_single_tenant(db):
    conn.set_schemas(['bolivia'])
    assert len(PartnersPartnerorganization.objects.all()) == RECORDS


def test_query_multi_tenant(db):
    conn.set_schemas(['bolivia', 'chad'])
    assert len(PartnersPartnerorganization.objects.all()) == RECORDS * 2


def test_count_single_tenant(db):
    conn.set_schemas(['bolivia'])
    assert PartnersPartnerorganization.objects.count() == RECORDS


def test_count_multi_tenant1(db):
    conn.set_schemas(['bolivia', 'chad'])
    assert PartnersPartnerorganization.objects.count() == RECORDS * 2


def test_count_multi_tenant2(db):
    conn.set_schemas(['bolivia', 'chad'])
    assert PartnersPartnerorganization.objects.count() == RECORDS * 2


@pytest.mark.parametrize("schema", [['bolivia'], ['bolivia', 'chad']])
def test_select_order(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.only('id',
                                    'name').order_by('id',
                                                     'name')
    for obj in qs:
        assert obj.name


@pytest.mark.parametrize("schema", [['bolivia'], ['bolivia', 'chad']])
def test_select_related(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.only('id',
                                    'name',
                                    'result_type').select_related('result_type').order_by('id',
                                                                                          'name')
    for obj in qs:
        assert obj.result_type.name


@pytest.mark.parametrize("schema", [['bolivia'], ['bolivia', 'chad']])
def test_mixed_schema(db, schema):
    conn.set_schemas(schema)
    qs = ActionPointsActionpoint.objects.only('assigned_by').select_related('assigned_by')
    for obj in qs:
        assert obj.assigned_by.username


@pytest.mark.parametrize("schema", [['bolivia'], ['bolivia', 'chad']])
def test_latest(db, schema):
    conn.set_schemas(schema)
    obj = ReportsResult.objects.all().latest('id')
    assert obj.name


@pytest.mark.parametrize("schema", [['bolivia'], ['bolivia', 'chad']])
def test_filtering(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.filter(id__gt=10).order_by('id', 'name')
    for obj in qs:
        assert obj.name


@pytest.mark.parametrize("schema", [['bolivia'], ['bolivia', 'chad']])
def test_prefetch_related(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.only('id',
                                    'name',
                                    'result_type').prefetch_related('result_type')
    for obj in qs:
        assert obj.result_type.name
