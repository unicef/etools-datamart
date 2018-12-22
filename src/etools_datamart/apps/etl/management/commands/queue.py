from django.core.management.base import CommandError, LabelCommand
from django.utils.module_loading import import_string

from django_extensions.management.utils import signalcommand


class Command(LabelCommand):
    requires_system_checks = False
    help = "Trigger celery with selected task"
    args = "[task]"
    label = 'task'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar=self.label, nargs='*')

    @signalcommand
    def handle_label(self, task, **options):
        from celery import current_app
        tasks = list(sorted(name for name in current_app.tasks
                            if not name.startswith('celery.')))

        if task not in tasks:
            self.stdout.write("\n".join(tasks))
            raise CommandError(f"'{task}' is not a registered Celery task")

        cmd = import_string(task)
        cmd.delay()
