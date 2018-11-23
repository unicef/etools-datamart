import io

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from etools_datamart.apps.data.models import UserStats
from etools_datamart.apps.etl.tasks.etl import load_user_report


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    assert client.login(username='admin', password='password')
    return client


def test_1(db, client, settings):
    load_user_report.unlock()
    load_user_report()
    assert UserStats.objects.count()

    url = reverse("api:userstats-list")
    res = client.get(f"{url}?format=xlsx")

    from storages.backends.azure_storage import AzureStorage
    storage = AzureStorage()
    storage.save('test1.xlsx', io.BytesIO(res.content))
