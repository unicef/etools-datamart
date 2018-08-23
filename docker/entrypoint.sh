#!/bin/bash -e
set -e


if [ "$@" == "datamart" ];then
    mkdir -p /var/datamart/{static,log,conf,run,redis}
    rm -f /var/datamart/run/*

    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 1

    django-admin db-isready --wait --timeout 300 --connection etools
    if [ "$STACK" == "1" ];then
        exec supervisord --nodaemon
    else
        if [ "$DEVELOPMENT_MODE" == "1" ];then
            python /code/manage.py runserver 0.0.0.0:8000
        else
            gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi
        fi
    fi
else
    exec "$@"
fi
