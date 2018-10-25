import unicef_rest_framework
import unicef_security

from etools_datamart.apps.init.checks import check_imports


def test_datamart():
    check_imports()


def test_unicef_rest_framework():
    check_imports(unicef_rest_framework)


def test_unicef_security():
    check_imports(unicef_security)
