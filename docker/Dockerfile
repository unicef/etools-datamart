ARG BASE_IMAGE

#FROM byrnedo/alpine-curl:0.1.7 as loader
#
#ARG BUILD_DATE
#ARG VERSION
#ARG DEVELOP
#ARG GITHUB_TOKEN

#ENV DEVELOP=${DEVELOP}
#ENV GITHUB_TOKEN=${GITHUB_TOKEN}
#ENV DATAMART_VERSION=${VERSION}
#
#RUN mkdir -p /code
#COPY . /code
#WORKDIR /code
#RUN set -o pipefail && \
#    if [ "${DEVELOP}" = "1" ]; then \
#    echo "${VERSION}-develop"; \
#    else \
#    echo "Download package: https://github.com/unicef/etools-datamart/archive/${DATAMART_VERSION}.tar.gz" \
#    && curl -L -u "${GITHUB_TOKEN}:" "https://github.com/unicef/etools-datamart/archive/${DATAMART_VERSION}.tar.gz" | tar -xzf - --strip-components=1; \
#    fi

FROM unicef/datamart-base:${BASE_IMAGE}
#COPY --from=loader /code /code

ARG BUILD_DATE
ARG PIPENV_ARGS
ARG VERSION
ARG DEVELOP

ENV DEVELOP=${DEVELOP}
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV DATAMART_VERSION=${VERSION}

RUN mkdir -p /code
COPY . /code
WORKDIR /code
RUN set -o pipefail && \
    if [ "${DEVELOP}" = "1" ]; then \
    echo "${VERSION}-develop"; \
    else \
    echo "Download package: https://github.com/unicef/etools-datamart/archive/${DATAMART_VERSION}.tar.gz" \
    && curl -L -u "https://github.com/unicef/etools-datamart/archive/${DATAMART_VERSION}.tar.gz" | tar -xzf - --strip-components=1; \
    fi
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
    ALLOWED_HOSTS="*" \
    CACHE_URL="redis://127.0.0.1:6379/1" \
    CELERY_AUTOSCALE="5,1" \
    CELERY_BROKER_URL="redis://127.0.0.1:6379/2" \
    CELERY_LOGLEVEL="ERROR" \
    CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/3" \
    CELERY_EXTRA="" \
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

ENV UWSGI_PROTOCOL=http \
    UWSGI_WORKERS=4 \
    UWSGI_AUTO_PROCNAME=true \
    UWSGI_BUFFER_SIZE=32768 \
    UWSGI_DIE_ON_TERM=true \
    UWSGI_DISABLE_LOGGING=false \
    UWSGI_DISABLE_WRITE_EXCEPTION=true \
    UWSGI_FREEBIND=true \
    UWSGI_HTTP_TIMEOUT=60 \
    UWSGI_IGNORE_SIGPIPE=true \
    UWSGI_IGNORE_WRITE_ERRORS=true \
    UWSGI_LIMIT_POST=20971520 \
    UWSGI_LOG_X_FORWARDED_FOR=false \
    UWSGI_MEMORY_REPORT=true \
    UWSGI_NEED_APP=true \
    UWSGI_POST_BUFFERING=65536 \
    UWSGI_PROCNAME_PREFIX_SPACED="[Datamart]" \
    UWSGI_RELOAD_ON_RSS=600 \
    UWSGI_THREADS=4 \
    UWSGI_THUNDER_LOCK=true \
    UWSGI_VACUUM=true \
    UWSGI_MODULE="etools_datamart.config.wsgi:application" \
    UWSGI_HTTP_SOCKET=0.0.0.0:8000 \
    UWSGI_MASTER=true \
    UWSGI_ENABLE_THREADS=true \
    UWSGI_LAZY_APPS=true \
    UWSGI_SINGLE_INTERPRETER=true

EXPOSE 8000

ADD docker/*.sh /usr/local/bin/
ADD docker/circus.conf /etc/

RUN addgroup --gid 1024 datamart \
    && adduser --disabled-password --ingroup datamart -S datamart

ENTRYPOINT ["entrypoint.sh"]
WORKDIR /var/datamart

CMD ["datamart"]
