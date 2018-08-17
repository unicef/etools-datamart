CMD?=
TARGET?=dev
DOCKER_IMAGE=unicef/datamart:${TARGET}
DOCKERFILE?=docker/Dockerfile
BUILD_OPTIONS?=
DATABASE_URL?=postgres://postgres:@192.168.66.66:5432/etools_datamart
DATABASE_URL_ETOOLS?=postgis://postgres:@192.168.66.66:15432/etools
PYPI_INDEX?=https://pypi.org/simple/

#builder:
#	cd .. && docker build ${BUILD_OPTIONS} \
#			--target builder \
#			--build-arg PYPI_SERVER=${PYPI_SERVER} \
#			--build-arg PYPI_INDEX=${PYPI_INDEX} \
#			-t ${DOCKER_IMAGE} \
#			-f ${DOCKERFILE} .

build:
	cd .. && docker build ${BUILD_OPTIONS} \
			--build-arg PYPI_INDEX=${PYPI_INDEX} \
			--build-arg GITHUB_TOKEN=${GITHUB_TOKEN} \
			-t ${DOCKER_IMAGE} \
			-f ${DOCKERFILE} .

run:
	cd .. && docker run \
	 		--rm \
			-p 8000:8000 \
			-p 5555:5555 \
			-e CACHE_URL=redis://127.0.0.1:6379/1 \
			-e CELERY_BROKER_URL=redis://127.0.0.1:6379/2 \
			-e CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/3 \
			-e CSRF_COOKIE_SECURE=false \
			-e DATABASE_URL=${DATABASE_URL} \
			-e DATABASE_URL_ETOOLS=${DATABASE_URL_ETOOLS} \
			-e DEBUG=true \
			-e DJANGO_SETTINGS_MODULE=etools_datamart.config.settings \
			-e SECURE_BROWSER_XSS_FILTER=0 \
			-e SECURE_CONTENT_TYPE_NOSNIFF=0 \
			-e SECURE_FRAME_DENY=0 \
			-e SECURE_HSTS_SECONDS=0 \
			-e SECURE_HSTS_PRELOAD=false \
			-e SECURE_SSL_REDIRECT=false \
			-e SERVICES="redis,workers,beat,datamart" \
			-e SESSION_COOKIE_HTTPONLY=false \
			-e SESSION_COOKIE_SECURE=false \
			-e STATIC_ROOT=/var/datamart/static/ \
			-e DEVELOPMENT_MODE=0 \
			-e USE_GUNICORN=1 \
			-e X_FRAME_OPTIONS="SAMEORIGIN" \
			-v $$PWD/~build/volumes/var/datamart:/var/datamart/ \
			-it ${DOCKER_IMAGE} \
			${CMD}

test:
	CMD='django-admin check --deploy' $(MAKE) run

shell:
	CMD='/bin/bash' $(MAKE) run
