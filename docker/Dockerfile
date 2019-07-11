FROM unicef/datamart-base:1.3

ARG BUILD_DATE
ARG PIPENV_ARGS
ARG VERSION
ARG DEVELOP

RUN mkdir -p /code
ADD . /code
WORKDIR /code

RUN set -ex \
    ls -al /code \
    && pip3 install . \
    && rm -fr /code


LABEL org.label.name="eTools Datamart" \
      org.label.maintainer="sapostolico@unicef.org" \
      org.label.description="" \
      org.label.url="https://datamart.unicef.io/" \
      org.label.vcs-url="https://github.com/unicef/etools-datamart" \
      org.label.version=$VERSION


ENV VERSION ${VERSION}

ENV PIPENV_PYPI_MIRROR=${PIPENV_PYPI_MIRROR}, \
    PIPENV_ARGS=${PIPENV_ARGS}, \
    HOME=/root/ \
    PYTHONUNBUFFERED=1 \
    USE_GUNICORN=0 \
    GUNICORN_WORKERS=4 \
    GUNICORN_TIMEOUT=300 \
    CELERY_LOGLEVEL="ERROR" \
    CELERY_CONCURRENCY=2 \
    CELERY_WORKERS=1 \
    ALLOWED_HOSTS="*" \
    CACHE_URL="redis://127.0.0.1:6379/1" \
    CELERY_BROKER_URL="redis://127.0.0.1:6379/2" \
    CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/3" \
    CSRF_COOKIE_SECURE=True \
    DATABASE_URL="postgres://postgres:@127.0.0.1:5432/etools_datamart" \
    DATABASE_URL_ETOOLS="postgis://postgres:@127.0.0.1:5432/etools" \
    DEBUG=0 \
    DEVELOPMENT_MODE=0 \
    DJANGO_SETTINGS_MODULE=etools_datamart.config.settings \
    MEDIA_ROOT=/tmp/media \
    SECRET_KEY="secret" \
    SECURE_BROWSER_XSS_FILTER=True \
    SECURE_CONTENT_TYPE_NOSNIFF=True \
    SECURE_FRAME_DENY=True \
    SECURE_HSTS_INCLUDE_SUBDOMAINS=True \
    SECURE_HSTS_PRELOAD=True \
    SECURE_HSTS_SECONDS=1 \
    SECURE_SSL_REDIRECT=True \
    SENTRY_DSN="" \
    SESSION_COOKIE_HTTPONLY=True \
    SESSION_COOKIE_SECURE=True \
    STATIC_ROOT=/tmp/static


EXPOSE 8000

ADD docker/*.sh /usr/local/bin/

RUN adduser -S datamart \
    && mkdir -p /var/datamart \
    && chown datamart /var/datamart/

ENTRYPOINT ["entrypoint.sh"]
WORKDIR /var/datamart

USER datamart

CMD ["datamart"]
