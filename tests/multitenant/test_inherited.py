from django.db import connections

import pytest

from etools_datamart.apps.sources.etools.models import (
    AuditAudit,
    AuditMicroassessment,
    AuditSpecialaudit,
    AuditSpotcheck,
)

conn = connections['etools']


@pytest.mark.parametrize("model", [AuditSpotcheck, AuditAudit,
                                   AuditMicroassessment, AuditSpecialaudit])
def test_spotcheck(db, model):
    # lebanon, bolivia, kenya
    conn.set_schemas(['bolivia'])
    assert model.objects.all().count() >= 0
    instance = model.objects.first()
    if instance:
        assert instance.engagement_ptr
