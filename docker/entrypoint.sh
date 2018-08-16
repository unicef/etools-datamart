#!/bin/bash -e
set -e

if [ "$@" == "datamart" ];then
    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all
    if [ "$USE_GUNICORN" == "1" ];then
        gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi
    else
        python /code/manage.py runserver 0.0.0.0:8000
    fi
else
    exec "$@"
fi
