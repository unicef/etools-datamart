#!/bin/bash -e
set -e


if [ "$@" == "datamart" ];then
    mkdir -p /var/datamart/{static,log,conf,run,redis}

    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 1

    if [ "$DEVELOPMENT_MODE" == "1" ];then
        echo "DEVELOPMENT_MODE set. supervisord not started"
        if [ "$USE_GUNICORN" == "1" ];then
            gunicorn -b 0.0.0.0:8000 etools_datamart.config.wsgi
        else
            python /code/manage.py runserver 0.0.0.0:8000
        fi
    else
        if [ -n "$SERVICES" ]; then
            supervisord -c /var/datamart/conf/supervisord.conf
            supervisorctl -c /var/datamart/conf/supervisord.conf start ${SERVICES//,/ }
        else
            echo "Empty 'SERVICES' environment. supervisord not started"
            echo "$SERVICES"
        fi
    fi
else
    exec "$@"
fi
