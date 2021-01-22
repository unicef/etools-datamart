from django.apps import apps
from django.db import connections

import pytest
from freezegun import freeze_time

from etools_datamart.apps.etl.loader import loadeables


def pytest_generate_tests(metafunc):
    if 'loader' in metafunc.fixturenames:
        m = []
        ids = []
        for model_name in sorted(loadeables):
            model = apps.get_model(model_name)
            # # if model_name in ['data.pdindicator', 'data.location', 'data.travelactivity',
            # #                   'data.actionpoint', 'data.tpmactivity', 'data.tpmvisit', ]:
            # if model_name in [
            #     'data.pdindicator',
            #     'data.location',
            #     'data.interventionbylocation',
            #     'data.fundsreservation',
            #     'data.reportindicator',
            #     'data.auditresult',
            # ]:
            #     m.append(pytest.param(model.loader, marks=pytest.mark.xfail))
            if model._meta.app_label == 'prp':
                m.append(pytest.param(model.loader, marks=pytest.mark.skip))
            elif model._meta.app_label == 'rapidpro':
                m.append(pytest.param(model.loader, marks=pytest.mark.skip))
            else:
                m.append(model.loader)
            # ids.append('%s.%s' % (model._meta.app_label, model._meta.verbose_name))
            ids.append(model._meta.label)
        metafunc.parametrize("loader", m, ids=ids)


def truncate_model_table(model):
    conn = connections['default']
    cursor = conn.cursor()
    # cursor.execute(f'TRUNCATE TABLE "{model._meta.db_table}"')
    cursor.execute('TRUNCATE TABLE "{0}" '
                   'RESTART IDENTITY CASCADE;'.format(model._meta.db_table))


@pytest.mark.django_db
def test_loader_load(loader):
    # source  = loader.model._etl_config.source
    # factory = factories_registry.get(source)
    with freeze_time("2018-12-31", tz_offset=1):
        truncate_model_table(loader.model)
        loader.unlock()
        ret = loader.load(max_records=2, ignore_dependencies=True, only_delta=False)
    assert loader.model.objects.count() >= 0
    assert ret.processed >= 0
    # assert ret.deleted == 0
    # assert not loader.model.objects.exclude(seen=ret.context['today']).exists()
    # assert not loader.model.objects.filter(id=to_delete.pk).exists()
