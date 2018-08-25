import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools_datamart.config.settings')


class DatamartCelery(Celery):

    def gen_task_name(self, name, module):
        prefix = ""
        if module.endswith('.tasks.etl'):
            module = module[:-10]
            # prefix = 'etl_'
        if module.endswith('.tasks'):
            module = module[:-6]
        return prefix + super(DatamartCelery, self).gen_task_name(name, module)


app = DatamartCelery('datamart')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(related_name='tasks')
app.autodiscover_tasks(related_name='etl')
