#!/bin/bash -e
mkdir -p /var/datamart/static
mkdir -p /var/datamart/log
mkdir -p /var/datamart/conf
mkdir -p /var/datamart/run

chown datamart:datamart -R /var/datamart/


if [[ "$*" == "worker" ]];then
    django-admin db-isready --wait --sleep 5 --timeout 60
    django-admin db-isready --wait --sleep 5 --timeout 300 --connection etools
    exec gosu datamart celery worker \
            -A etools_datamart \
            --events \
            --max-tasks-per-child=1 \
            --loglevel=${CELERY_LOGLEVEL} \
            --autoscale=${CELERY_AUTOSCALE} \
            --pidfile run/celery.pid \
            $CELERY_EXTRA


elif [[ "$*" == "beat" ]];then
    exec gosu datamart celery beat -A etools_datamart.celery \
            $CELERY_EXTRA \
            --loglevel=${CELERY_LOGLEVEL} \
            --pidfile run/celerybeat.pid

elif [[ "$*" == "w2" ]];then
    django-admin db-isready --wait --timeout 60
    exec gosu datamart circusd /etc/circus.conf --log-output=-

elif [[ "$*" == "datamart" ]];then
    rm -f /var/datamart/run/*

    django-admin diffsettings --output unified
#    django-admin makemigrations --check --dry-run

    django-admin db-isready --wait --timeout 60
    django-admin check --deploy
    django-admin init-setup --all --verbosity 2
    django-admin db-isready --wait --timeout 300 --connection etools
    echo "uwsgi --static-map ${STATIC_URL}=${STATIC_ROOT}"
    exec gosu datamart uwsgi --static-map ${STATIC_URL}=${STATIC_ROOT}
else
    exec "$@"
fi
