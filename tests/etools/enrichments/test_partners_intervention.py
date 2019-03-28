import pytest

from etools_datamart.apps.etools.models import PartnersIntervention

pytestmark = pytest.mark.django_db


def test_intervention_location():
    i = PartnersIntervention.objects.first()
    assert i.flat_locations.all()


def test_intervention_frs():
    i = PartnersIntervention.objects.first()
    assert i.frs.all()
