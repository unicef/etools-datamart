#!/bin/bash -e
set -e

mkdir -p /var/datamart/{static,log,conf,run,redis}
rm -f /var/datamart/run/*


if [ "$*" == "celery" ];then
    export START_REDIS="false"
    export START_DATAMART="false"
    export START_CELERY="true"

    django-admin db-isready --wait --timeout 60 --sleep 5
    django-admin db-isready --wait --timeout 300  --sleep 5 --connection etools

    cd /var/datamart

    exec supervisord --nodaemon
elif [ "$*" == "datamart" ];then

    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 1
    django-admin db-isready --wait --timeout 300 --connection etools

    if [ "$DEVELOPMENT_MODE" == "1" ];then
        python /code/manage.py runserver 0.0.0.0:8000
    else
        gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi
    fi
elif [ "$*" == "stack" ];then
    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 1
    django-admin db-isready --wait --timeout 300 --connection etools

    cd /var/datamart
    exec supervisord --nodaemon
else
    exec "$@"
fi
