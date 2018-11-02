import pytest


@pytest.mark.parametrize('flt', ['country_name=bolivia', 'country_name=', 'country_name=bolivia,chad'])
def test_filter_etools_country_name(db, client, flt):
    url = f"/api/etools/audit/engagement/?%s" % flt
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()


@pytest.mark.parametrize('flt', ['country_name=bolivia', 'country_name=', 'country_name=bolivia,chad'])
def test_filter_datamart_country_name(db, client, flt):
    url = f"/api/datamart/interventions/?%s" % flt
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()


@pytest.mark.parametrize('flt', ['10', 'oct', '10-2018', 'current'])
def test_filter_datamart_month(db, client, flt):
    url = f"/api/datamart/user-stats/?month=%s" % flt
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()
