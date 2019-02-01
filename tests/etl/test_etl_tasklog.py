import pytest

from unicef_security.models import User

from etools_datamart.apps.data.models import HACT
from etools_datamart.apps.etl.models import EtlTask

pytestmarker = pytest.mark.django_db


def test_manager(db):
    # TaskLogFactory(content_type=ContentType.objects.get_for_model(HACT))
    assert EtlTask.objects.filter_for_models(HACT)
    assert EtlTask.objects.get_for_model(HACT)
    with pytest.raises(EtlTask.DoesNotExist):
        assert EtlTask.objects.get_for_model(User)
