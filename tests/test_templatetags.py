# -*- coding: utf-8 -*-
from unittest.mock import Mock

from django.contrib.contenttypes.models import ContentType

from etools_datamart.apps.subscriptions.templatetags.subscriptions import subscription_select
from etools_datamart.apps.web.templatetags.datamart import server_ip


def test_server_ip():
    request = Mock(get_host=lambda: "localhost:8000")
    assert server_ip({"request": request}) == "localhost"


def test_subscription_select(admin_user, ):
    ct = ContentType.objects.first()
    assert subscription_select({'user': admin_user}, Mock(content_type=ct))
