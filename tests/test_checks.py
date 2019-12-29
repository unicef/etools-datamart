from unittest import mock

from etools_datamart.apps.mart.data.checks import check_loader


def test_checks():
    assert check_loader(None) == []


def test_checks_fail():
    with mock.patch('etools_datamart.apps.mart.data.models.intervention.Intervention.loader.config.last_modify_field',
                    'aaaa'):
        assert check_loader(None)
