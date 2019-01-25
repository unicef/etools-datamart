# -*- coding: utf-8 -*-
from django.apps import apps

from freezegun import freeze_time

from etools_datamart.apps.data.loader import loadeables


def pytest_generate_tests(metafunc):
    if 'loader' in metafunc.fixturenames:
        m = []
        ids = []
        for model_name in loadeables:
            model = apps.get_model(model_name)
            m.append(model.loader)
            ids.append(model.__name__)
        metafunc.parametrize("loader", m, ids=ids)


def test_loader_load(loader, number_of_intervention):
    # factory = factories_registry.get(loader.model)
    # to_delete = factory()
    with freeze_time("2018-12-31", tz_offset=1):
        loader.model.objects.truncate()
        loader.unlock()
        ret = loader.load(max_records=2, force_requirements=True)
    assert loader.model.objects.count()
    assert not loader.model.objects.exclude(seen=ret.context['today']).exists()
    # assert not loader.model.objects.filter(id=to_delete.pk).exists()

# def test_load_pmp_indicator(number_of_intervention):
#     PMPIndicators.objects.truncate()
#     PMPIndicators.loader.unlock()
#     assert PMPIndicators.loader.load() == EtlResult(created=153)
#     assert PMPIndicators.objects.count() == number_of_intervention * 3
#
#
# def test_load_intervention(number_of_intervention, settings, monkeypatch):
#     Intervention.loader.unlock()
#     assert Intervention.loader.load() == EtlResult(created=number_of_intervention * 3)
#     assert Intervention.objects.count() == number_of_intervention * 3
#
#
# def test_load_fam_indicator(db, settings, monkeypatch):
#     FAMIndicator.loader.unlock()
#     FAMIndicator.loader.load()
#     assert FAMIndicator.objects.count() == 3
#
#
# def test_load_user_stats(db, settings, monkeypatch):
#     UserStats.loader.unlock()
#     UserStats.loader.load()
#     assert UserStats.objects.count() == 3
#
#
# def test_load_location(db, settings, monkeypatch):
#     Location.loader.unlock()
#     Location.loader.load()
#     assert UserStats.objects.count() == 3
#
#
# def test_load_hact(db, settings, monkeypatch):
#     HACT.loader.unlock()
#     HACT.loader.load()
#     assert HACT.objects.count() == 3
#     bolivia = HACT.objects.get(country_name='Bolivia')
#     assert bolivia.microassessments_total == 0
#     assert bolivia.programmaticvisits_total == 1
#     assert bolivia.followup_spotcheck == 0
#     assert bolivia.completed_spotcheck == 0
#     assert bolivia.completed_hact_audits == 0
#     assert bolivia.completed_special_audits == 0
#     res = HACT.loader.load()
#     assert res == EtlResult(unchanged=3)
#
#
# @freeze_time("2018-11-10")
# def test_dataset_increased(db, settings, monkeypatch):
#     UserStats.loader.unlock()
#     UserStats.loader.load()
#     UserStats.objects.first().delete()
#     ret = UserStats.loader.load()
#     assert ret == EtlResult(created=1, unchanged=2)
#
#
# @freeze_time("2018-11-10")
# def test_dataset_changed(db, settings, monkeypatch):
#     UserStats.loader.unlock()
#     ret = UserStats.loader.load()
#     assert ret == EtlResult(created=3)
#     UserStats.objects.update(total=999, unicef=999)
#
#     ret = UserStats.loader.load()
#     assert ret == EtlResult(updated=3)
