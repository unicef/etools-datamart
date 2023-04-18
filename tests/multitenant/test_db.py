from django.db import connections

import pytest

from etools_datamart.apps.sources.etools.models import (
    ActionPointsActionpoint,
    AuthGroup,
    PartnersPartnerorganization,
    ReportsResult,
)

conn = connections["etools"]

pytestmark = pytest.mark.django_db

PARTNER_ORGANIZATION_COUNT = 77


def test_query_public(db):
    conn.set_schemas(["bolivia"])
    assert AuthGroup.objects.all()


def test_query_single_tenant(number_of_partnerorganization):
    conn.set_schemas(["bolivia"])
    assert len(PartnersPartnerorganization.objects.all()) == PARTNER_ORGANIZATION_COUNT


def test_query_multi_tenant(number_of_partnerorganization):
    conn.set_schemas(["bolivia", "chad"])
    assert len(PartnersPartnerorganization.objects.all()) == number_of_partnerorganization


def test_count_single_tenant(number_of_partnerorganization):
    conn.set_schemas(["bolivia"])
    assert PartnersPartnerorganization.objects.count() == PARTNER_ORGANIZATION_COUNT


def test_count_multi_tenant1(number_of_partnerorganization):
    conn.set_schemas(["bolivia", "chad"])
    assert PartnersPartnerorganization.objects.count() == number_of_partnerorganization


def test_count_multi_tenant2(number_of_partnerorganization):
    conn.set_schemas(["bolivia", "chad"])
    assert PartnersPartnerorganization.objects.count() == number_of_partnerorganization


@pytest.mark.parametrize("schema", [["bolivia"], ["bolivia", "chad"]])
def test_select_order(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.only("id", "name").order_by("id", "name")
    for obj in qs:
        assert obj.name


@pytest.mark.parametrize("schema", [["bolivia"], ["bolivia", "chad"]])
def test_select_related(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.only("id", "name", "result_type").select_related("result_type").order_by("id", "name")
    for obj in qs:
        assert obj.result_type.name


@pytest.mark.parametrize("schema", [["bolivia"], ["bolivia", "chad"]])
def test_mixed_schema(db, schema):
    conn.set_schemas(schema)
    qs = ActionPointsActionpoint.objects.only("assigned_by").select_related("assigned_by")
    for obj in qs:
        assert obj.assigned_by.username


@pytest.mark.parametrize("schema", [["bolivia"], ["bolivia", "chad"]])
def test_latest(db, schema):
    conn.set_schemas(schema)
    obj = ReportsResult.objects.all().latest("id")
    assert obj.name


@pytest.mark.parametrize("schema", [["bolivia"], ["bolivia", "chad"]])
def test_filtering(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.filter(id__gt=10).order_by("id", "name")
    for obj in qs:
        assert obj.name


@pytest.mark.parametrize("schema", [["bolivia"], ["bolivia", "chad"]])
def test_prefetch_related(db, schema):
    conn.set_schemas(schema)
    qs = ReportsResult.objects.only("id", "name", "result_type").prefetch_related("result_type")
    for obj in qs:
        assert obj.result_type.name
