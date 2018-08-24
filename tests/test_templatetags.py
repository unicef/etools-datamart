# -*- coding: utf-8 -*-
from unittest.mock import Mock

from etools_datamart.apps.core.templatetags.datamart import server_ip


def test_server_ip():
    request = Mock(get_host=lambda: "localhost:8000")
    assert server_ip({"request": request}) == "localhost"
