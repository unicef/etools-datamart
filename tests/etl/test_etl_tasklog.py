from etools_datamart.apps.etl.models import TaskLog
from etools_datamart.apps.etl.tasks import load_pmp_indicator


def test_load_pmp_indicator(db):
    TaskLog.objects.filter().delete()
    assert not TaskLog.objects.exists()
    assert load_pmp_indicator.apply()
    assert TaskLog.objects.filter(task='etl_etools_datamart.apps.etl.load_pmp_indicator').exists()
