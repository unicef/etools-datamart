import pytest
from django.db import models
from django.utils.functional import cached_property

from etools_datamart.apps.etools.enrichment.utils import create_alias
from etools_datamart.apps.etools.models import PartnersIntervention, LocationsLocation, \
    PartnersInterventionFlatLocations
pytestmark = pytest.mark.django_db


def test_intervention_location():
    i = PartnersIntervention.objects.first()
    assert i.flat_locations.all()


def test_intervention_frs():
    i = PartnersIntervention.objects.first()
    assert i.frs.all()

