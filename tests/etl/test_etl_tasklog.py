import pytest

from etools_datamart.apps.core.models import User
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.mart.data.models import HACT

pytestmarker = pytest.mark.django_db


def test_manager(db):
    # TaskLogFactory(content_type=ContentType.objects.get_for_model(HACT))
    assert EtlTask.objects.filter_for_models(HACT)
    assert EtlTask.objects.get_for_model(HACT)
    with pytest.raises(EtlTask.DoesNotExist):
        assert EtlTask.objects.get_for_model(User)
