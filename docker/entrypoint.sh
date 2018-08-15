#!/bin/bash -e
set -e

if [ ! -f /var/datamart/.bootstrapped ]; then
    touch /var/datamart/.bootstrapped
    echo "done"
fi

if [ "$@" == "sir" ];then
    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --deploy
    if [ "$USE_GUNICORN" == "1" ];then
        gunicorn -b 0.0.0.0:8000 sir.config.wsgi
    else
        python /code/manage.py runserver 0.0.0.0:8000
    fi
else
    exec "$@"
fi
