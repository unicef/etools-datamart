BUILD_OPTIONS?=
CMD?=datamart
TARGET?=dev
DEVELOP?=0
CONTAINER_NAME?=datamart-${TARGET}
DATABASE_URL?=postgres://postgres:@192.168.66.66:5432/etools_datamart
DATABASE_URL_ETOOLS?=postgis://postgres:@192.168.66.66:15432/etools
DOCKER_IMAGE_NAME=unicef/datamart
DOCKER_IMAGE=${DOCKER_IMAGE_NAME}:${TARGET}
DOCKERFILE?=Dockerfile
RUN_OPTIONS?=

help:
	@echo "dev                  build dev image (based on local code)"
	@echo "build                build production image (based on tag ${TARGET})"
	@echo "release              release tag ${TARGET} on docker hub"
	@echo "run                  run ${DOCKER_IMAGE} locally"


build:
	cd .. && docker build ${BUILD_OPTIONS} \
			--build-arg DEVELOP=${DEVELOP} \
			--build-arg GITHUB_CREDENTIALS=${GITHUB_CREDENTIALS} \
			--build-arg VERSION=${TARGET} \
			-t ${DOCKER_IMAGE} \
			-f docker/${DOCKERFILE} .
	docker images | grep ${DOCKER_IMAGE_NAME}

.run:
	cd .. && docker run \
	 		--rm \
	 		--name=${CONTAINER_NAME} \
			-p 8000:8000 \
			-p 5555:5555 \
			-p 15000:15000 \
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
			-e SESSION_COOKIE_HTTPONLY=false \
			-e SESSION_COOKIE_SECURE=false \
			-e STATIC_ROOT=/var/datamart/static/ \
			-e DEVELOPMENT_MODE=0 \
			-e STACK=1 \
			-e X_FRAME_OPTIONS="SAMEORIGIN" \
			-v $$PWD/~build/volumes/var/datamart:/var/datamart/ \
			${RUN_OPTIONS} \
			${DOCKER_IMAGE} \
			${CMD}

local:
	RUN_OPTIONS="-v ${PWD}/..:/code -e PYTHONPATH=/code -it" \
	CMD="/bin/bash" \
	$(MAKE) .run

release:
	docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
	docker tag ${DOCKER_IMAGE_NAME}:${TARGET} ${DOCKER_IMAGE_NAME}:latest
	docker push ${DOCKER_IMAGE_NAME}:latest
	docker push ${DOCKER_IMAGE_NAME}:${TARGET}

run:
	$(MAKE) .run

test:
	RUN_OPTIONS="-e DEBUG=0 \
				 -e X_FRAME_OPTIONS=DENY \
				 -e SESSION_COOKIE_SECURE=1 \
				 -e CSRF_COOKIE_SECURE=1 \
				 -e SECURE_HSTS_PRELOAD=1 \
				 -e SECURE_SSL_REDIRECT=1" \
	CMD='bash -c "django-admin check --deploy"' \
	$(MAKE) .run

scratch:
	RUN_OPTIONS=-it CMD='/bin/bash' $(MAKE) .run

shell:
#	docker exec -it ${CONTAINER_NAME} /bin/bash
	RUN_OPTIONS=-it CMD='/bin/bash' $(MAKE) .run
