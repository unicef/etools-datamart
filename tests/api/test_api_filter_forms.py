from etools_datamart.api.endpoints import FundsReservationViewSet, InterventionViewSet, PMPIndicatorsViewSet


def test_filter_form1(db, django_app, admin_user):
    service = PMPIndicatorsViewSet.get_service()
    url = service.endpoint
    res = django_app.get(url, user=admin_user, headers={'Accept': 'text/html'})
    assert res.status_code == 200
    url = f"{service.endpoint}?partner_type__in=&pd_ssfa_status__in="
    res = django_app.get(url, user=admin_user, headers={'Accept': 'text/html'})
    assert res.status_code == 200


def test_filter_form2(db, django_app, admin_user):
    service = InterventionViewSet.get_service()
    url = service.endpoint
    res = django_app.get(url, user=admin_user, headers={'Accept': 'text/html'})
    assert res.status_code == 200
    url = f"{service.endpoint}?status__in="
    res = django_app.get(url, user=admin_user, headers={'Accept': 'text/html'})
    assert res.status_code == 200


def test_filter_form3(db, django_app, admin_user):
    service = FundsReservationViewSet.get_service()
    url = service.endpoint
    res = django_app.get(url, user=admin_user, headers={'Accept': 'text/html'})
    assert res.status_code == 200
    url = f"{service.endpoint}?status__in="
