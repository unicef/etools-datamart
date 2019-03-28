from django.db import connections

import pytest

conn = connections['etools']


@pytest.fixture(autouse=True)
def setup_conn():
    conn.set_schemas(["bolivia"])
