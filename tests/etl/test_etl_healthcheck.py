from etools_datamart.apps.etl.tasks import healthcheck


def test_healthcheck_async():
    healthcheck.apply()


def test_healthcheck():
    healthcheck()
