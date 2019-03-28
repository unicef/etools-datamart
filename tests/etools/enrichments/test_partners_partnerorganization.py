import pytest

from etools_datamart.apps.etools.models import PartnersPartnerorganization

pytestmark = pytest.mark.django_db


def test_spotchecks():
    i = PartnersPartnerorganization.objects.first()
    assert i.spotchecks.all()
