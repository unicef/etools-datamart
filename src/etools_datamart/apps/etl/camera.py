from datetime import timedelta

from django.db.transaction import get_connection, TransactionManagementError
from django.utils import timezone

from celery import states
from celery.events.snapshot import Polaroid
from celery.utils.imports import symbol_by_name
from celery.utils.log import get_logger

from etools_datamart.libs.time import fromtimestamp

WORKER_UPDATE_FREQ = 60  # limit worker timestamp write freq.
SUCCESS_STATES = frozenset([states.SUCCESS])

logger = get_logger(__name__)
debug = logger.debug


class Camera(Polaroid):
    """The Celery events Polaroid snapshot camera."""

    clear_after = True
    worker_update_freq = WORKER_UPDATE_FREQ

    def __init__(self, *args, **kwargs):
        super(Camera, self).__init__(*args, **kwargs)
        # Expiry can be timedelta or None for never expire.
        self.app.add_defaults({
            'monitors_expire_success': timedelta(days=1),
            'monitors_expire_error': timedelta(days=3),
            'monitors_expire_pending': timedelta(days=5),
        })

    @property
    def TaskState(self):
        """Return the data model to store task state in."""
        return symbol_by_name('etools_datamart.apps.etl.models.EtlTask')

    def django_setup(self):
        import django
        django.setup()

    def install(self):
        super(Camera, self).install()
        self.django_setup()

    def handle_task(self, uuid_task, worker=None):
        """Handle snapshotted event."""
        uuid, task = uuid_task

        defaults = {
            'task': task.name,
            'task_id': uuid,
            'status': task.state,
            'last_run': fromtimestamp(task.timestamp),
            'results': task.result or task.exception,
            'traceback': task.traceback,
            'elapsed': task.runtime
        }
        if task.state == states.STARTED:
            pass
        elif task.state == states.SUCCESS:
            defaults['last_success'] = timezone.now()
            defaults['last_failure'] = None
            defaults['task_id'] = None
        elif task.state == states.FAILURE:
            defaults['last_failure'] = timezone.now()
            defaults['task_id'] = None
        elif task.state == states.RETRY:
            defaults['task_id'] = None
            defaults['last_failure'] = timezone.now()
        print("{0.name:>25} {0.state}".format(task))
        if get_connection().in_atomic_block:
            raise TransactionManagementError("Cannot use DurableAtomic inside Atomic")
        self.TaskState.objects.filter(task=task.name).update(**defaults)

    def on_shutter(self, state):
        for i, task in enumerate(state.tasks.items()):
            self.handle_task(task)

    # def on_cleanup(self):
