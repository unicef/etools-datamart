from django.db import connections

import pytest

conn = connections["etools"]


@pytest.fixture(autouse=True)
def setup_conn(db):
    conn.set_schemas(["bolivia"])
