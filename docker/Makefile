CMD?=
TARGET?=dev
DOCKER_IMAGE=unicef/datamart:${TARGET}
DOCKERFILE?=docker/Dockerfile
BUILD_OPTIONS?=
DATABASE_URL?=postgres://postgres:@192.168.66.66:5432/etools_datamart
DATABASE_URL_ETOOLS?=postgis://postgres:@192.168.66.66:15432/etools

builder:
	cd .. && docker build ${BUILD_OPTIONS} \
			--target builder \
			--build-arg PYPI_SERVER=${PYPI_SERVER} \
			--build-arg PYPI_INDEX=${PYPI_INDEX} \
			-t ${DOCKER_IMAGE} \
			-f ${DOCKERFILE} .

build:
	cd .. && docker build ${BUILD_OPTIONS} \
			--build-arg GITHUB_TOKEN=${GITHUB_TOKEN} \
			-t ${DOCKER_IMAGE} \
			-f ${DOCKERFILE} .

run:
	cd .. && docker run -p 8000:8000 --rm \
			-e DATABASE_URL=${DATABASE_URL} \
			-e DATABASE_URL_ETOOLS=${DATABASE_URL_ETOOLS} \
			-e USE_GUNICORN=0 \
			-e DEBUG=true \
			-e SECURE_SSL_REDIRECT=false \
			-e SESSION_COOKIE_SECURE=false \
			-e SESSION_COOKIE_HTTPONLY=false \
			-e SESSION_COOKIE_HTTPONLY=false \
			-e CSRF_COOKIE_SECURE=false \
			-e STATIC_ROOT=/var/etools_datamart/static/ \
			-e DJANGO_SETTINGS_MODULE=etools_datamart.config.settings \
			-it ${DOCKER_IMAGE} \
			${CMD}

test:
	CMD='django-admin check --deploy' $(MAKE) run

shell:
	CMD='/bin/bash' $(MAKE) run
