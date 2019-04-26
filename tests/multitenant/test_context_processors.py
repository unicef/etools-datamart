from unittest.mock import Mock

from etools_datamart.apps.multitenant.context_processors import schemas


def test_schemas(db):
    assert schemas(Mock())
