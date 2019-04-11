#!/usr/bin/env bash

TAG=${1:-v6.9}

docker run \
    -it \
    -e SECRET_KEY=123 \
    -e DATABASE_URL=${DATABASE_URL_ETOOLS} \
    -e DJANGO_SETTINGS_MODULE=etools.config.settings.base \
    -e DJANGO_DEBUG=true \
    unicef/etools:$TAG \
    /bin/sh -c "django-admin migrate"
