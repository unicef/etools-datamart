from django.core.management.base import CommandError, LabelCommand
from django.utils.functional import cached_property


class Command(LabelCommand):
    requires_system_checks = []
    help = "Trigger celery with selected task"
    args = "[task]"
    label = "task"
    missing_args_message = "Enter at least one %s." % label

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.missing_args_message = "Enter at least one task %s: " % self.valid_tasks

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--wait",
            "-w",
            action="store_true",
            dest="wait",
            default=False,
            help="Wait task to be completed and display result",
        )

    @cached_property
    def valid_tasks(self):
        from celery import current_app

        return list(
            sorted(
                name
                for name in current_app.tasks
                # if not name.startswith('celery.')
            )
        )

    def handle_label(self, task, **options):
        if task not in self.valid_tasks:
            raise CommandError(f"'{task}' is not a registered Celery task. %s" % "\n".join(self.valid_tasks))

        from celery import current_app

        tsk = current_app.tasks[task]
        if options["wait"]:
            self.stdout.write("Running %s" % task)
            result = tsk.apply_async()
            self.stdout.write(str(result.get()))
        else:
            self.stdout.write("Queued %s" % task)
            tsk.delay()
