FROM python:3.6-slim as builder

ARG PYPI_SERVER="pypi.org"
ARG PYPI_INDEX="https://$PYPI_SERVER/simple/"

ENV PYPI_SERVER ${PYPI_SERVER}
ENV PYPI_INDEX ${PYPI_INDEX}

ENV HOME /root/
ENV PIPSI_HOME=/usr/local/pipsi/environments
ENV PIPSI_BIN_DIR=/usr/local/bin
ENV DEBUG 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE sir.config.settings
ENV PYTHONUNBUFFERED 1
ENV GUNICORN_CMD_ARGS "-b 0.0.0.0:8000 \
--chdir /var/sir \
--access-logfile - \
--access-logformat \"%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s\""
ENV SECURE_SSL_REDIRECT False
ENV ALLOWED_HOSTS *
ENV SECURE_SSL_REDIRECT False
ENV CSRF_COOKIE_SECURE False
ENV SECURE_HSTS_SECONDS False
ENV SECURE_HSTS_INCLUDE_SUBDOMAINS = True
ENV SECURE_FRAME_DENY False
ENV SESSION_COOKIE_SECURE False
ENV SESSION_COOKIE_HTTPONLY False
ENV SECURE_BROWSER_XSS_FILTER False
ENV SECURE_CONTENT_TYPE_NOSNIFF False

RUN apt-get update && apt-get install -y \
    curl

RUN mkdir -p /code /root/.local/bin \
    && pip install -U pip \
    && curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python \
    && pip install virtualenv \
    && pipsi install pipenv

WORKDIR /code
ADD . /code
RUN pipenv install -v --system --deploy \
    && pip install -e .

RUN mkdir -p /var/datamart/
WORKDIR /var/datamart
VOLUME /var/datamart/

ADD docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["sir"]
