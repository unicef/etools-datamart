import pytest

from etools_datamart.apps.etools.models import PartnersPartnerorganization

pytestmark = pytest.mark.django_db


def test_planned_engagement(setup_conn):
    i = PartnersPartnerorganization.objects.first()
    assert i.planned_engagement.spot_check_planned_q1 >= 0
