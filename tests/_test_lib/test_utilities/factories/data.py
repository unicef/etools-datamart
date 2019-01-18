import random
from datetime import datetime

from django.db import connections
from django.utils import timezone

import factory
from factory.fuzzy import BaseFuzzyAttribute
from test_utilities.factories import today
from test_utilities.factories.common import RegisterModelFactory

from etools_datamart.apps.data.models import (FAMIndicator, GatewayType, HACT, Intervention,
                                              Location, PMPIndicators, UserStats,)


class DataMartModelFactory(RegisterModelFactory):
    schema_name = factory.Iterator(connections['etools'].get_tenants())
    country_name = factory.SelfAttribute('schema_name')


class HACTFactory(DataMartModelFactory):
    year = today.year
    country_name = factory.SelfAttribute('schema_name')

    class Meta:
        model = HACT


class PMPIndicatorFactory(DataMartModelFactory):
    # schema_name = factory.Iterator(connections['etools'].get_tenants())
    class Meta:
        model = PMPIndicators
        django_get_or_create = ('country_name',)


class FAMIndicatorFactory(DataMartModelFactory):
    month = today
    last_modify_date = timezone.now()

    class Meta:
        model = FAMIndicator


class InterventionFactory(DataMartModelFactory):
    metadata = {}
    title = factory.Sequence(lambda n: "title%03d" % n)
    number = factory.Sequence(lambda n: "#%03d" % n)
    partner_contribution = 10
    unicef_cash = 10
    in_kind_amount = 10
    partner_contribution_local = 10
    unicef_cash_local = 10
    in_kind_amount_local = 10
    total = 10
    total_local = 10
    currency = 'USD'

    class Meta:
        model = Intervention


class GatewayTypeFactory(DataMartModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = GatewayType
        django_get_or_create = ('name',)


class LocationFactory(DataMartModelFactory):
    gateway = factory.SubFactory(GatewayTypeFactory)
    name = factory.Sequence(lambda n: "name%03d" % n)
    level = factory.Sequence(lambda n: n)
    lft = 1
    rght = 1
    tree_id = 1
    created = timezone.now()
    modified = timezone.now()
    is_active = True

    class Meta:
        model = Location
        django_get_or_create = ('name',)


class FuzzyMonth(BaseFuzzyAttribute):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fuzz(self):
        return datetime(today.year, random.choice([1, 2, 3]), 1)  # noqa


class UserStatsFactory(DataMartModelFactory):
    month = FuzzyMonth()

    class Meta:
        model = UserStats
        django_get_or_create = ('month', 'country_name')
