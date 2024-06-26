# unicef/etools-prp-base:latest
#ARG BASE_TAG=installed
ARG BASE_TAG=latest
FROM unicef/datamart:$BASE_TAG

ADD src /code/
ADD manage.py /code/manage.py

WORKDIR /code/
RUN apk add bash

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

# CLEANUP
# Disabled for now, till move to etools-base
# See https://github.com/unicef/etools/pull/2716
# RUN apk del .build-deps

RUN python manage.py collectstatic --noinput

EXPOSE 8000
