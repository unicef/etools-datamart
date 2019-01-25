FROM pstauffer/curl:latest as builder
ARG DEVELOP
ARG GITHUB_CREDENTIALS
ARG VERSION

RUN mkdir /code
ADD . /code

RUN set -o pipefail && if [ "${DEVELOP}" = "1" ]; then \
    echo "${VERSION}-develop"; \
    else \
    echo "Download package: https://github.com/unicef/etools-datamart/archive/${VERSION}.tar.gz" \
    && curl ${GITHUB_CREDENTIALS}: -L "https://github.com/unicef/etools-datamart/archive/${VERSION}.tar.gz" | tar -xzf - --strip-components=1; \
    fi

FROM python:3.6.7-slim as base
RUN apt-get update \
 	&& apt-get install -y --no-install-recommends \
 	    gcc \
 	    gdal-bin \
 	    python-dev


RUN pip install pip==18.0 pipenv --upgrade \
    && adduser --system datamart

FROM base
COPY --from=builder /code /code

LABEL org.label.name="eTools Datamart" \
      org.label.maintainer="sapostolico@unicef.org" \
      org.label.description="" \
      org.label.url="https://datamart.unicef.io/" \
      org.label.vcs-url="https://github.com/unicef/etools-datamart" \
      org.label.version=$VERSION


ARG BUILD_DATE
ARG PIPENV_ARGS
ARG VERSION

ENV VERSION ${VERSION}
ENV ABSOLUTE_BASE_URL "http://datamart.unicef.io"
ENV PIPENV_PYPI_MIRROR ${PIPENV_PYPI_MIRROR}
ENV PIPENV_ARGS ${PIPENV_ARGS}
ENV HOME /root/
ENV PIPSI_HOME=/usr/local/pipsi/environments
ENV PIPSI_BIN_DIR=/usr/local/bin
ENV PYTHONUNBUFFERED 1
ENV USE_GUNICORN 0
ENV GUNICORN_CMD_ARGS " -b 0.0.0.0:8000 \
--name datamart \
--chdir /var/datamart \
--access-logfile - \
--timeout 120 \
--access-logformat \"%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s\" "

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
ENV SESSION_COOKIE_HTTPONLY True
ENV SESSION_COOKIE_SECURE True
ENV STATIC_ROOT /tmp/static
#ENV SUPERVISOR_USER admin
#ENV SUPERVISOR_PWD ""
#ENV FLOWER_USER admin
#ENV FLOWER_PWD ""
#ENV X_FRAME_OPTIONS "DENY"
#ENV START_DATAMART "true"
#ENV START_REDIS "true"
#ENV START_CELERY "true"

#RUN apt-get update && apt-get install -y --force-yes \
#    gcc

RUN mkdir -p \
    /var/datamart/ \
    && chown datamart /var/datamart/ \
    && pip install pip==18.0 pipenv --upgrade

WORKDIR /code

RUN set -ex \
    ls -al /code \
    && pipenv install --verbose --system --deploy --ignore-pipfile $PIPENV_ARGS

RUN pip install . \
    && rm -fr /code \
    && mkdir -p /var/datamart/ \
    && chown -R datamart /var/datamart/


#RUN apk del .build-deps \
#    && rm -rf /var/cache/apk/* \
#    && rm -fr /root/.cache/

WORKDIR /var/datamart

EXPOSE 8000

USER datamart

ADD docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["datamart"]
