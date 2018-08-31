# -*- coding: utf-8 -*-
import pytest
from rest_framework.test import APIClient
from unicef_rest_framework.models import Service

from etools_datamart.api.endpoints import InterventionViewSet


@pytest.fixture()
def client(admin_user):
    client = APIClient()
    assert client.login(username='admin', password='password')
    return client


@pytest.fixture()
def service(db):
    Service.objects.load_services()
    return Service.objects.order_by('?').first()


@pytest.fixture()
def data_service(db):
    Service.objects.load_services()
    return Service.objects.filter(viewset=InterventionViewSet).order_by('?').first()
