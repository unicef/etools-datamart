from django.core.management import call_command

from etools_datamart.celery import app


@app.task(name='send_queued_mail')
def send_queued_mail():
    call_command('send_queued_mail')
