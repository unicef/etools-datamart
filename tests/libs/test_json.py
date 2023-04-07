from datetime import datetime
from decimal import Decimal
from unittest import mock

import pytest

from etools_datamart.libs.json import print_json

data = {"decimal": Decimal(1.0), "date": datetime.today(), "string": "str"}


@pytest.mark.parametrize("obj", [data, (data,), "str"])
def test_print_json(obj):
    with mock.patch("etools_datamart.libs.json.sys.stdout") as stdout:
        print_json(obj)
        stdout.write.assert_called_once()
