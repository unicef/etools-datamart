import random
from datetime import datetime

from django.db import connections
from django.utils import timezone

import factory
from factory.fuzzy import BaseFuzzyAttribute
from test_utilities.factories import today
from test_utilities.factories.common import RegisterModelFactory

from etools_datamart.apps.data.models import (ActionPoint, EtoolsUser, FAMIndicator, FundsReservation,
                                              GatewayType, HACT, Intervention, InterventionByLocation,
                                              Location, Partner, PDIndicator, PMPIndicators,
                                              TPMActivity, TPMVisit, Travel, TravelActivity, UserStats,)


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
    intervention_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Intervention


class InterventionByLocationFactory(DataMartModelFactory):
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
    intervention_id = factory.Sequence(lambda n: n)

    class Meta:
        model = InterventionByLocation


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


class FundsReservationFactory(DataMartModelFactory):
    intervention = factory.SubFactory(InterventionFactory)
    actual_amt = 101
    intervention_amt = 102
    outstanding_amt = 103
    total_amt = 104
    actual_amt_local = 105
    outstanding_amt_local = 106
    multi_curr_flag = False
    line_item = 1
    overall_amount = 107
    overall_amount_dc = 108
    created = timezone.now()
    modified = timezone.now()

    source_id = 1
    source_intervention_id = 1

    class Meta:
        model = FundsReservation


class PDIndicatorFactory(DataMartModelFactory):
    is_active = True
    is_high_frequency = True

    class Meta:
        model = PDIndicator


class TravelFactory(DataMartModelFactory):
    created = timezone.now()

    class Meta:
        model = Travel


class PartnerFactory(DataMartModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)
    blocked = False
    created = timezone.now()
    description = ""
    manually_blocked = False
    vision_synced = True
    deleted_flag = False
    hidden = False

    class Meta:
        model = Partner


class TravelActivityFactory(DataMartModelFactory):
    travel_reference_number = factory.Sequence(lambda n: "name%03d" % n)

    # blocked = False
    # created = timezone.now()
    # description = ""
    # manually_blocked = False
    # vision_synced = True
    # deleted_flag = False
    # hidden = False

    class Meta:
        model = TravelActivity


class ActionPointFactory(DataMartModelFactory):
    class Meta:
        model = ActionPoint


class TPMActivityFactory(DataMartModelFactory):
    class Meta:
        model = TPMActivity


class TPMVisitFactory(DataMartModelFactory):
    class Meta:
        model = TPMVisit


class EtoolsUserFactory(DataMartModelFactory):
    is_superuser = False
    username = factory.Sequence(lambda n: "username%03d" % n)
    email = factory.Sequence(lambda n: "email%03d@example.com" % n)

    class Meta:
        model = EtoolsUser
