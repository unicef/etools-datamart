# envs to set before use this script
DATABASE_URL?=
DATABASE_URL_ETOOLS?=
DEVELOP?=0
DOCKER_PASS?=
DOCKER_USER?=
TARGET?=1.23.0a7
BASE=1.3
# below vars are used internally
BUILD_OPTIONS?=--squash
CMD?=datamart
CONTAINER_NAME?=datamart-${TARGET}
ORGANIZATION=unicef
IMAGE_NAME=datamart
DOCKER_IMAGE_NAME?=${ORGANIZATION}/${IMAGE_NAME}
DOCKER_IMAGE?=${DOCKER_IMAGE_NAME}:${TARGET}
DOCKERFILE?=Dockerfile
RUN_OPTIONS?=
PIPENV_ARGS?=
PORTS=
ABSOLUTE_BASE_URL?="http://192.168.66.66:8000"

help:
	@echo "dev                  build dev image (based on local code)"
	@echo "build                build production image (based on tag ${TARGET})"
	@echo "release              release tag ${TARGET} on docker hub"
	@echo "run                  run ${DOCKER_IMAGE} locally"

build-base:
	cd .. && docker build \
			${BUILD_OPTIONS} \
			--no-cache \
			-t ${DOCKER_IMAGE_NAME}-base:${BASE} \
			-f docker/Dockerfile.base .


.build:
	cd .. && docker build \
			${BUILD_OPTIONS} \
			--build-arg PIPENV_ARGS=${PIPENV_ARGS} \
			-t ${DOCKER_IMAGE} \
			-f docker/Dockerfile .
	docker tag ${DOCKER_IMAGE_NAME}:${TARGET} ${DOCKER_IMAGE_NAME}:dev
	docker images | grep ${DOCKER_IMAGE_NAME}

build-test:
	TARGET=dev $(MAKE) .build test

build:
	$(MAKE) .build test

build_old:
	cd .. && docker build \
			${BUILD_OPTIONS} \
			--build-arg DEVELOP=${DEVELOP} \
			--build-arg VERSION=${TARGET} \
			--build-arg PIPENV_ARGS=${PIPENV_ARGS} \
			-t ${DOCKER_IMAGE} \
			-f docker/Dockerfile.flat .
	docker tag ${DOCKER_IMAGE_NAME}:${TARGET} ${DOCKER_IMAGE_NAME}:dev
	docker images | grep ${DOCKER_IMAGE_NAME}


.run:
	cd .. && docker run \
	 		--rm \
	 		--name=${CONTAINER_NAME} \
			-e ABSOLUTE_BASE_URL=${ABSOLUTE_BASE_URL} \
			-e CACHE_URL=redis://192.168.66.66:6379/1 \
			-e CACHE_URL_API=redis://192.168.66.66:6379/2 \
			-e CACHE_URL_LOCK=redis://192.168.66.66:6379/3 \
			-e CACHE_URL_TEMPLATE=redis://192.168.66.66:6379/4 \
			-e CELERY_BROKER_URL=redis://192.168.66.66:6379/2 \
			-e CELERY_RESULT_BACKEND=redis://192.168.66.66:6379/3 \
			-e CSRF_COOKIE_SECURE=false \
			-e DATABASE_URL=${DATABASE_URL} \
			-e DATABASE_URL_ETOOLS=${DATABASE_URL_ETOOLS} \
			-e DEBUG=false \
			-e DJANGO_SETTINGS_MODULE=etools_datamart.config.settings \
			-e SECURE_BROWSER_XSS_FILTER=0 \
			-e SECURE_CONTENT_TYPE_NOSNIFF=0 \
			-e SECURE_FRAME_DENY=0 \
			-e SECURE_HSTS_SECONDS=0 \
			-e SECURE_HSTS_PRELOAD=false \
			-e SECURE_SSL_REDIRECT=false \
			-e SESSION_COOKIE_HTTPONLY=false \
			-e SESSION_COOKIE_SECURE=false \
			-e STATIC_ROOT=/var/datamart/static/ \
			-e DEVELOPMENT_MODE=0 \
			-e X_FRAME_OPTIONS="SAMEORIGIN" \
			${RUN_OPTIONS} \
			${DOCKER_IMAGE} \
			${CMD}

local:
	RUN_OPTIONS="-v ${PWD}/..:/code -e PYTHONPATH=/code -it" \
	CMD="/bin/bash" \
	$(MAKE) .run

release:
	@echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
	docker tag ${DOCKER_IMAGE_NAME}:${TARGET} ${DOCKER_IMAGE_NAME}:latest
	docker push ${DOCKER_IMAGE_NAME}:${TARGET}

deploy:
	lazo rancher upgrade datamart:datamart ${DOCKER_IMAGE_NAME}:${TARGET}
	lazo rancher upgrade datamart:celery ${DOCKER_IMAGE_NAME}:${TARGET}
	lazo rancher upgrade datamart:beat ${DOCKER_IMAGE_NAME}:${TARGET}
#	$(MAKE) bump

bump:
	cd .. && bumpversion --commit --tag --config-file=.bumpversion.cfg num

run:
	RUN_OPTIONS="-p 8000:8000" \
		ABSOLUTE_BASE_URL=${ABSOLUTE_BASE_URL} \
		$(MAKE) .run

stack:
	RUN_OPTIONS="-p 8000:8000" \
		CMD=stack \
		ABSOLUTE_BASE_URL=${ABSOLUTE_BASE_URL} \
		$(MAKE) .run

workers:
	CONTAINER_NAME=datamart-workers \
			ABSOLUTE_BASE_URL=${ABSOLUTE_BASE_URL} \
			CMD=worker $(MAKE) .run

beat:
	CONTAINER_NAME=datamart-beat \
		ABSOLUTE_BASE_URL=${ABSOLUTE_BASE_URL} \
		CMD=beat $(MAKE) .run


test:
	RUN_OPTIONS="-e DEBUG=0 \
				 -e X_FRAME_OPTIONS=DENY \
				 -e SESSION_COOKIE_SECURE=1 \
				 -e CSRF_COOKIE_SECURE=1 \
				 -e SECURE_HSTS_PRELOAD=1 \
				 -e SECURE_SSL_REDIRECT=1" \
	CMD='bash -c "touch /var/datamart/.touch && django-admin check --deploy "' \
	$(MAKE) .run

scratch:
	RUN_OPTIONS=-it CMD='/bin/bash' $(MAKE) .run

shell:
	RUN_OPTIONS="-p 8000:8000 -it" \
		ABSOLUTE_BASE_URL=${ABSOLUTE_BASE_URL} \
	CMD='/bin/bash' \
		$(MAKE) .run
#	docker exec -it ${CONTAINER_NAME} /bin/bash
#	RUN_OPTIONS=-it CMD='/bin/bash' $(MAKE) .run

docker-remove:
	docker-remove.sh ${IMAGE_NAME} -o ${ORGANIZATION}

