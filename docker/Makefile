CMD?=
TARGET?=dev
DOCKER_IMAGE=unicef/eToolsDataMart:${TARGET}
DOCKERFILE?=docker/Dockerfile.${TARGET}
BUILD_OPTIONS?=

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
			-e DEBUG=true \
			-e SECURE_SSL_REDIRECT=false \
			-e SESSION_COOKIE_SECURE=false \
			-e SESSION_COOKIE_HTTPONLY=false \
			-e SESSION_COOKIE_HTTPONLY=false \
			-e CSRF_COOKIE_SECURE=false \
			-e STATIC_ROOT=/var/sir/static/ \
			-e DJANGO_SETTINGS_MODULE=sir.config.settings \
			-v $$PWD/~build/volumes/var/sir/:/var/sir/ \
			-it ${DOCKER_IMAGE} \
			${CMD}

test:
#	CMD="\"sh -c \'python -c \\\"import sir\'\\\"\"" $(MAKE) run
	CMD='django-admin check --deploy' $(MAKE) run
