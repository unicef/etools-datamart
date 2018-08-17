FROM python:3.6-slim as builder

ARG PYPI_INDEX="https://pypi.org/simple/"

ENV PYPI_INDEX ${PYPI_INDEX}

ENV HOME /root/
ENV PIPSI_HOME=/usr/local/pipsi/environments
ENV PIPSI_BIN_DIR=/usr/local/bin
ENV PYTHONUNBUFFERED 1
ENV USE_GUNICORN 0
ENV GUNICORN_CMD_ARGS "-b 0.0.0.0:8000 \
--chdir /var/datamart \
--access-logfile - \
--access-logformat \"%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s\""

ENV ALLOWED_HOSTS *
ENV CACHE_URL "redis://127.0.0.1:6379/1"
ENV CELERY_BROKER_URL "redis://127.0.0.1:6379/2"
ENV CELERY_RESULT_BACKEND "redis://127.0.0.1:6379/3"
ENV CSRF_COOKIE_SECURE True
ENV DATABASE_URL "postgres://postgres:@127.0.0.1:5432/etools_datamart"
ENV DATABASE_URL_ETOOLS "postgis://postgres:@127.0.0.1:5432/etools"
ENV DEBUG 0
ENV DEVELOPMENT_MODE 0
ENV DJANGO_SETTINGS_MODULE etools_datamart.config.settings
ENV MEDIA_ROOT /tmp/media
ENV SECRET_KEY "secret"
ENV SECURE_BROWSER_XSS_FILTER True
ENV SECURE_CONTENT_TYPE_NOSNIFF True
ENV SECURE_FRAME_DENY True
ENV SECURE_HSTS_INCLUDE_SUBDOMAINS True
ENV SECURE_HSTS_PRELOAD True
ENV SECURE_HSTS_SECONDS 1
ENV SECURE_SSL_REDIRECT True
ENV SENTRY_DSN ""
ENV SERVICES "redis,workers,beat"
ENV SESSION_COOKIE_HTTPONLY True
ENV SESSION_COOKIE_SECURE True
ENV STATIC_ROOT /tmp/media
ENV X_FRAME_OPTIONS "DENY"

RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    redis-server

RUN mkdir -p /code /root/.local/bin \
    && pip install -U pip \
    && curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python \
    && pip install virtualenv \
    && pipsi install pipenv

#FROM python:3.6-slim
#COPY --from=0 /root /root

WORKDIR /code
ADD . /code

RUN pipenv install -v --system --deploy --pypi-mirror $PYPI_INDEX \
    && pip install -e .

RUN mkdir -p /var/datamart/{static,log,conf,run}

ADD docker/redis.conf /etc/redis.conf
ADD docker/supervisord.conf /etc/supervisord.conf

WORKDIR /var/datamart

ADD docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["datamart"]
