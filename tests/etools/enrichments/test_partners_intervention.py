import pytest

from etools_datamart.apps.sources.etools.models import PartnersIntervention, PartnersInterventionFlatLocations

pytestmark = pytest.mark.django_db


def test_intervention_location():
    base = PartnersInterventionFlatLocations.objects.first()
    if base:
        assert base.intervention.flat_locations.all()


def test_intervention_frs():
    i = PartnersIntervention.objects.first()
    assert i.frs.all().count() >= 0


def test_intervention_sections():
    i = PartnersIntervention.objects.first()
    assert i.sections.all()
