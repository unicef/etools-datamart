#!/usr/bin/env bash
set -ex

TAG=${1:-7.4}

# from 6.9 to 6.10
# django-admin migrate --fake core 0001
# django-admin migrate core
# django-admin migrate --fake reports 0016


docker run \
    -it \
    -e SECRET_KEY=123 \
    -e DATABASE_URL=${DATABASE_URL_ETOOLS} \
    -e DJANGO_SETTINGS_MODULE=etools.config.settings.base \
    -e DJANGO_DEBUG=true \
    unicef/etools:$TAG \
    /bin/sh -c "django-admin migrate"
