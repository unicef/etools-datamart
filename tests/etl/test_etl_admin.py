from django.contrib import messages
from django.urls import reverse

import pytest
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from etools_datamart.apps.etl.models import EtlTask


@pytest.fixture
def tasklog():
    EtlTask.objects.inspect()
    return EtlTask.objects.first()


@pytest.fixture
def tasklog_scheduled(tasklog):
    midnight, __ = CrontabSchedule.objects.get_or_create(minute=0, hour=0)
    task = EtlTask.objects.latest()
    PeriodicTask.objects.get_or_create(task=task.task, defaults={"name": task.task, "crontab": midnight})


def test_tasklog_changelist(django_app, admin_user, tasklog_scheduled):
    url = reverse("admin:etl_etltask_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


# def test_tasklog_change(django_app, admin_user, tasklog):
#     url = reverse("admin:etl_etltask_change", args=[tasklog.id])
#     res = django_app.get(url, user=admin_user)
#     assert res.status_code == 200
#     res.form['last_run_0'] = '2000-01-01'
#     res = res.form.submit()
#     assert res.status_code == 302, f"Submit failed with: {repr(res.context['adminform'].errors)}"


def test_tasklog_unlock(django_app, admin_user, tasklog):
    url = reverse("admin:etl_etltask_change", args=[tasklog.id])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Unlock")
    res = res.forms[1].submit().follow()
    storage = res.context["messages"]
    assert [m.message for m in storage] == ["Successfully executed"]


def test_tasklog_queue(django_app, admin_user, tasklog):
    url = reverse("admin:etl_etltask_change", args=[tasklog.id])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Queue")
    res = res.follow()
    storage = res.context["messages"]
    assert [m.message for m in storage] == [f"Task '{tasklog.task}' queued"]


def test_tasklog_queue_action(django_app, admin_user, tasklog):
    tasklog.loader.task.delay = lambda **kw: True
    url = reverse("admin:etl_etltask_changelist")
    res = django_app.get(url, user=admin_user)
    res.forms["changelist-form"]["action"].value = "queue"
    res.forms["changelist-form"]["_selected_action"] = [tasklog.id]
    res = res.forms["changelist-form"].submit().maybe_follow()
    assert res.status_code == 200
    storage = res.context["messages"]
    assert storage
    # assert [m.message for m in storage] in [
    #     ["Task 'load_data_actionpoint' queued"], ['1 task queued']
    # ]


def test_tasklog_refresh(django_app, admin_user, tasklog):
    url = reverse("admin:etl_etltask_change", args=[tasklog.id])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_tasklog_inspect(django_app, admin_user, tasklog):
    url = reverse("admin:etl_etltask_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
    res = res.click("Inspect").maybe_follow()
    assert res.status_code == 200
    storage = res.context["messages"]
    assert [messages.DEFAULT_TAGS[m.level] for m in storage] == ["success"], [m.message for m in storage]
