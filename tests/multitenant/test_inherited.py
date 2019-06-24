import pytest
from django.db import connections

from etools_datamart.apps.etools.models import (AuditAudit, AuditMicroassessment,
                                                AuditSpecialaudit, AuditSpotcheck, )

conn = connections['etools']


@pytest.mark.parametrize("model", [AuditSpotcheck, AuditAudit,
                                   AuditMicroassessment, AuditSpecialaudit])
def test_spotcheck(db, model):
    # lebanon, bolivia, kenya
    conn.set_schemas(['bolivia'])
    assert model.objects.all()
    instance = model.objects.first()
    assert instance.engagement_ptr
