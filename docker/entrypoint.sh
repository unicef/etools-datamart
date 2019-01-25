#!/bin/bash -e
set -e

django-admin diffsettings --output unified
django-admin makemigrations --check --dry-run

if [[ "$*" == "workers" ]];then
    django-admin db-isready --wait --timeout 60 --sleep 5
    django-admin db-isready --wait --timeout 300  --sleep 5 --connection etools
    celery worker -A etools_datamart --loglevel=DEBUG --concurrency=4 --purge --pidfile run/celery.pid
elif [[ "$*" == "beat" ]];then
    celery beat -A etools_datamart.celery --loglevel=DEBUG --pidfile run/celerybeat.pid
elif [[ "$*" == "datamart" ]];then

    mkdir -p ${STATIC_ROOT}
    rm -f /var/datamart/run/*


    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 2
    django-admin db-isready --wait --timeout 300 --connection etools
    gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi
else
    exec "$@"
fi
