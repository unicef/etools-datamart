# -*- coding: utf-8 -*-
from django.apps import apps

import pytest
from freezegun import freeze_time

from etools_datamart.apps.etl.loader import loadeables


def pytest_generate_tests(metafunc):
    if 'loader' in metafunc.fixturenames:
        m = []
        ids = []
        for model_name in loadeables:
            model = apps.get_model(model_name)
            # if model_name in ['data.pdindicator', 'data.location', 'data.travelactivity',
            #                   'data.actionpoint', 'data.tpmactivity', 'data.tpmvisit', ]:
            if model_name in [
                'data.pdindicator',
                'data.location',
                'data.interventionbylocation',
                'data.fundsreservation',
                'data.reportindicator',
            ]:
                m.append(pytest.param(model.loader, marks=pytest.mark.xfail))
            elif model._meta.app_label == 'prp':
                m.append(pytest.param(model.loader, marks=pytest.mark.skip))
            elif model._meta.app_label == 'rapidpro':
                m.append(pytest.param(model.loader, marks=pytest.mark.skip))
            else:
                m.append(model.loader)
            # ids.append('%s.%s' % (model._meta.app_label, model._meta.verbose_name))
            ids.append(model._meta.label)
        metafunc.parametrize("loader", m, ids=ids)


def test_loader_load(loader, number_of_intervention):
    # factory = factories_registry.get(loader.model)
    # factory()
    with freeze_time("2018-12-31", tz_offset=1):
        loader.model.objects.truncate()
        loader.unlock()
        ret = loader.load(max_records=2, ignore_dependencies=True, only_delta=False)
    assert loader.model.objects.count()
    assert ret.processed == 2
    # assert ret.deleted == 0
    # assert not loader.model.objects.exclude(seen=ret.context['today']).exists()
    # assert not loader.model.objects.filter(id=to_delete.pk).exists()
