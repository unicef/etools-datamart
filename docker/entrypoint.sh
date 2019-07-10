#!/bin/bash -e
mkdir -p /var/datamart/static
mkdir -p /var/datamart/log
mkdir -p /var/datamart/conf
mkdir -p /var/datamart/run

if [[ $DAEMONIZE == '1' ]]; then
    CELERY_EXTRA='--detach'
    GUNICORN_EXTRA='--daemon'
fi

if [[ "$*" == "test" ]];then
    DAEMONIZE=1 docker-entrypoint.sh beat
    DAEMONIZE=1 docker-entrypoint.sh workers
    DAEMONIZE=1 docker-entrypoint.sh datamart
    wait-for-it.sh localhost:8000 -t 60 -- curl localhost:8000
    if [[ ! -f "run/celery.pid" ]]; then exit 1; fi
    if [[ ! -f "run/celerybeat.pid" ]]; then exit 1; fi

elif [[ "$*" == "worker" ]];then
    django-admin db-isready --wait --sleep 5 --timeout 60
    django-admin db-isready --wait --sleep 5 --timeout 300 --connection etools
    celery worker -A etools_datamart \
            --loglevel=${CELERY_LOGLEVEL} \
            --concurrency=${CELERY_CONCURRENCY} \
            --purge \
            --pidfile run/celery.pid \
            $CELERY_EXTRA \


elif [[ "$*" == "beat" ]];then
    celery beat -A etools_datamart.celery \
            $CELERY_EXTRA \
            --loglevel=${CELERY_LOGLEVEL} \
            --pidfile run/celerybeat.pid

elif [[ "$*" == "datamart" ]];then
    rm -f /var/datamart/run/*

    django-admin diffsettings --output unified
    django-admin makemigrations --check --dry-run

    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 2
    django-admin db-isready --wait --timeout 300 --connection etools
    gunicorn -b 0.0.0.0:8000 \
        $GUNICORN_EXTRA \
        --workers=${GUNICORN_WORKERS} \
        --chdir /var/datamart \
        --timeout ${GUNICORN_TIMEOUT} \
        --access-logfile - \
        --access-logformat "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s" \
        etools_datamart.config.wsgi
else
    exec "$@"
fi
