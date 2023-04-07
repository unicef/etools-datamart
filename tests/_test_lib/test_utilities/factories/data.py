import random
from datetime import datetime

from django.db import connections
from django.utils import timezone

import factory
import pytz
from factory.fuzzy import BaseFuzzyAttribute
from test_utilities.factories import today
from test_utilities.factories.common import RegisterModelFactory

from etools_datamart.apps.mart.data import models


class DataMartModelFactory(RegisterModelFactory):
    schema_name = factory.Iterator(connections["etools"].get_tenants())
    country_name = factory.SelfAttribute("schema_name")


class HACTFactory(DataMartModelFactory):
    year = today.year
    country_name = factory.SelfAttribute("schema_name")

    class Meta:
        model = models.HACT


class PMPIndicatorFactory(DataMartModelFactory):
    # schema_name = factory.Iterator(connections['etools'].get_tenants())
    class Meta:
        model = models.PMPIndicators
        django_get_or_create = ("country_name",)


class FAMIndicatorFactory(DataMartModelFactory):
    month = today
    last_modify_date = timezone.now()

    class Meta:
        model = models.FAMIndicator


class AgreementFactory(DataMartModelFactory):
    class Meta:
        model = models.Agreement


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
    currency = "USD"
    intervention_id = factory.Sequence(lambda n: n)
    locations_data = [
        dict(
            source_id="1",
            name="location.name",
            pcode="location.p_code",
            level="location.admin_level",
            levelname="location.admin_level_name",
            latitude="location.latitude",
            longitude="location.longitude",
        )
    ]

    class Meta:
        model = models.Intervention


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
    currency = "USD"
    intervention_id = factory.Sequence(lambda n: n)

    class Meta:
        model = models.InterventionByLocation


class LocationFactory(DataMartModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)
    level = factory.Sequence(lambda n: n)
    lft = 1
    rght = 1
    tree_id = 1
    created = timezone.now()
    modified = timezone.now()
    is_active = True

    class Meta:
        model = models.Location
        django_get_or_create = ("name",)


class LocationsiteFactory(DataMartModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)
    is_active = True

    class Meta:
        model = models.Locationsite
        django_get_or_create = ("name",)


class PseaAnswerFactory(DataMartModelFactory):
    class Meta:
        model = models.PseaAnswer


class PseaAssessmentFactory(DataMartModelFactory):
    class Meta:
        model = models.PseaAssessment


class FuzzyMonth(BaseFuzzyAttribute):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fuzz(self):
        return datetime(today.year, random.choice([1, 2, 3]), 1, tzinfo=pytz.UTC)  # noqa


class UserStatsFactory(DataMartModelFactory):
    month = FuzzyMonth()

    class Meta:
        model = models.UserStats
        django_get_or_create = ("month", "country_name")


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
        model = models.FundsReservation


class PDIndicatorFactory(DataMartModelFactory):
    is_active = True
    is_high_frequency = True
    target_denominator = 1.1

    class Meta:
        model = models.PDIndicator


class TravelFactory(DataMartModelFactory):
    created = timezone.now()

    class Meta:
        model = models.Travel


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
        model = models.Partner


class PartnerHACTFactory(DataMartModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = models.PartnerHact


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
        model = models.TravelActivity


class ActionPointFactory(DataMartModelFactory):
    class Meta:
        model = models.ActionPoint


class TPMActivityFactory(DataMartModelFactory):
    class Meta:
        model = models.TPMActivity


class TPMVisitFactory(DataMartModelFactory):
    class Meta:
        model = models.TPMVisit


class EtoolsUserFactory(DataMartModelFactory):
    is_superuser = False
    username = factory.Sequence(lambda n: "username%03d" % n)
    email = factory.Sequence(lambda n: "email%03d@example.com" % n)

    class Meta:
        model = models.EtoolsUser


class InterventionBudgetFactory(DataMartModelFactory):
    class Meta:
        model = models.InterventionBudget


class InterventionActivityFactory(DataMartModelFactory):
    class Meta:
        model = models.InterventionActivity


class InterventionCountryProgrammeFactory(DataMartModelFactory):
    class Meta:
        model = models.InterventionCountryProgramme


class InterventionEPDFactory(DataMartModelFactory):
    class Meta:
        model = models.InterventionEPD


class InterventionManagementBudgetFactory(DataMartModelFactory):
    budget_created = timezone.now()
    budget_modified = timezone.now()

    class Meta:
        model = models.InterventionManagementBudget


class InterventionPlannedVisitsFactory(DataMartModelFactory):
    year = datetime.now().year

    class Meta:
        model = models.InterventionPlannedVisits


class InterventionReviewFactory(DataMartModelFactory):
    review_created = timezone.now()
    review_modified = timezone.now()

    class Meta:
        model = models.InterventionReview


class OfficeFactory(DataMartModelFactory):
    class Meta:
        model = models.Office


class SectionFactory(DataMartModelFactory):
    class Meta:
        model = models.Section


class TripFactory(DataMartModelFactory):
    class Meta:
        model = models.Trip


class TravelTripFactory(DataMartModelFactory):
    class Meta:
        model = models.TravelTrip


class EngagementFactory(DataMartModelFactory):
    partner = {"name": "Partner1", "vendor_number": "123", "id": 100, "source_id": 101}

    class Meta:
        model = models.Engagement


class FMOntrackFactory(DataMartModelFactory):
    class Meta:
        model = models.FMOntrack


class FMOptionFactory(DataMartModelFactory):
    class Meta:
        model = models.FMOptions


class FMQuestionFactory(DataMartModelFactory):
    class Meta:
        model = models.FMQuestion


class GrantFactory(DataMartModelFactory):
    class Meta:
        model = models.Grant


class HACTHistoryFactory(DataMartModelFactory):
    class Meta:
        model = models.HACTHistory


class ReportIndicatorFactory(DataMartModelFactory):
    class Meta:
        model = models.ReportIndicator


class AttachmentFactory(DataMartModelFactory):
    class Meta:
        model = models.Attachment


class AuditResultFactory(DataMartModelFactory):
    audited_expenditure = 1.0
    financial_findings = 2.0
    audit_opinion = "--"

    class Meta:
        model = models.AuditResult


class SpotCheckFindingsFactory(DataMartModelFactory):
    partner = {"name": "Partner1", "vendor_number": "123", "id": 100, "source_id": 101}

    class Meta:
        model = models.SpotCheckFindings


class MicroAssessmentFactory(DataMartModelFactory):
    partner = {"name": "Partner1", "vendor_number": "123", "id": 100, "source_id": 101}

    class Meta:
        model = models.MicroAssessment


class AuditFactory(DataMartModelFactory):
    partner = {"name": "Partner1", "vendor_number": "123", "id": 100, "source_id": 101}

    class Meta:
        model = models.Audit


class AuditFinancialFindingFactory(DataMartModelFactory):
    created = timezone.now()
    local_amount = 100.0
    amount = 200.0

    class Meta:
        model = models.AuditFinancialFinding


class AuditSpecialFactory(DataMartModelFactory):
    partner = {"name": "Partner1", "vendor_number": "123", "id": 100, "source_id": 101}

    class Meta:
        model = models.AuditSpecial


class PartnerStaffMemberFactory(DataMartModelFactory):
    class Meta:
        model = models.PartnerStaffMember


class ResultFactory(DataMartModelFactory):
    class Meta:
        model = models.Result
