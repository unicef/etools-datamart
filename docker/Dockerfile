FROM python:3.6.8-alpine3.8

ARG BUILD_DATE
ARG PIPENV_ARGS
ARG VERSION
ARG DEVELOP

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

RUN apk add --no-cache --virtual .fetch-deps \
        curl
#        ca-certificates \
#        openssl \
#        tar

RUN apk add --no-cache --virtual .build-deps \
        autoconf \
        automake \
        pkgconf \
        g++ \
        json-c-dev \
        libtool \
        libxml2-dev \
        make \
        perl

RUN apk add --no-cache --virtual .build-deps-edge \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        proj4-dev \
        protobuf-c-dev

RUN apk add --no-cache --virtual .postgis-rundeps \
        json-c

RUN apk add --no-cache --virtual .postgis-rundeps-edge \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        binutils \
        geos \
        geos-dev \
        gdal-dev \
        gdal \
        proj4 \
        protobuf-c

RUN apk add --no-cache --virtual .datamart-build-deps \
        freetype-dev \
        fontconfig-dev \
        freetype-dev \
        jpeg-dev \
        lcms2-dev \
        libffi-dev \
        libressl-dev \
        linux-headers \
        musl-dev \
        openjpeg-dev \
        postgresql-dev \
        python3-dev \
        tcl-dev \
        tiff-dev \
        tk-dev \
        zlib-dev

RUN apk add --no-cache --virtual .datamart-run-deps \
        postgresql-libs

RUN apk add --no-cache --virtual .system-run-deps \
        bash

RUN mkdir -p /code
ADD . /code
WORKDIR /code

RUN set -o pipefail && echo "DEVELOP: ${DEVELOP}" && if [ "${DEVELOP}" == "1" ]; then \
    echo "${VERSION}-develop"; \
    else \
    echo "Download package: https://github.com/unicef/etools-datamart/archive/${VERSION}.tar.gz" \
    && curl -L "https://github.com/unicef/etools-datamart/archive/${VERSION}.tar.gz" | tar -xzf - --strip-components=1; \
    fi

RUN pip install pip==18.0 pipenv --upgrade


RUN set -ex \
    ls -al /code \
    && pipenv install --verbose --system --deploy --ignore-pipfile $PIPENV_ARGS \
    && pip3 install . \
    && rm -fr /code

LABEL org.label.name="eTools Datamart" \
      org.label.maintainer="sapostolico@unicef.org" \
      org.label.description="" \
      org.label.url="https://datamart.unicef.io/" \
      org.label.vcs-url="https://github.com/unicef/etools-datamart" \
      org.label.version=$VERSION


ENV VERSION ${VERSION}

ENV PIPENV_PYPI_MIRROR ${PIPENV_PYPI_MIRROR}
ENV PIPENV_ARGS ${PIPENV_ARGS}
ENV HOME /root/
ENV PIPSI_HOME=/usr/local/pipsi/environments
ENV PIPSI_BIN_DIR=/usr/local/bin
ENV PYTHONUNBUFFERED 1
ENV USE_GUNICORN 0
ENV GUNICORN_CMD_ARGS "-b 0.0.0.0:8000 \
--chdir /var/datamart \
--access-logfile - \
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


EXPOSE 8000
RUN apk del .fetch-deps .build-deps .build-deps-edge .datamart-build-deps
RUN rm -rf /var/cache/apk/* \
    rm -fr /root/.cache/ \
    rm -fr /code \
    rm -fr /usr/include/

RUN find /usr/local/lib/python3.6/ -name *.pyc | xargs rm -f \
    && python -O -m compileall -fqb /usr/local/lib/python3.6/ \
    && find /usr/local/lib/python3.6/ -name *.py | xargs rm -f

ADD docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN adduser -S datamart \
    && mkdir -p /var/datamart \
    && chown datamart /var/datamart/

WORKDIR /var/datamart
USER datamart

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["datamart"]
