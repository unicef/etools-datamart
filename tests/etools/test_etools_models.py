# test various patch
from django.db import connections

import pytest

from etools_datamart.apps.etools.models import PartnersIntervention

pytestmark = pytest.mark.django_db

conn = connections['etools']


@pytest.fixture(autouse=True)
def setup_conn():
    conn.set_schemas(["bolivia"])


def test_intervention_location():
    i = PartnersIntervention.objects.first()
    assert i.flat_locations.all()
