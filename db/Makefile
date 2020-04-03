DB_DUMP_LOCATION?=/tmp/psql_data/db2.bz2
DOCKER_IMAGE=unicef/etools-db:dev2
VOLUME_ETOOLS_DATA?=/Users/Shared/data/storage/etools-db/data
VOLUME_ETOOLS_BACKUP?=/Users/Shared/data/storage/etools-db/dumps

build:
	docker build \
		-t ${DOCKER_IMAGE} \
		-f Dockerfile .


clean:
	docker rmi ${DOCKER_IMAGE}

init:
	docker run --rm -it \
			-e DB_DUMP_LOCATION=${DB_DUMP_LOCATION} \
			-v ${VOLUME_ETOOLS_BACKUP}:/tmp/psql_data/ \
			-v ${VOLUME_ETOOLS_DATA}:/var/lib/postgresql/data \
			${DOCKER_IMAGE}

restore:
	docker run --rm -it \
			-e DB_DUMP_LOCATION=${DB_DUMP_LOCATION} \
			-v ${VOLUME_ETOOLS_BACKUP}:/tmp/psql_data/ \
			-v ${VOLUME_ETOOLS_DATA}:/var/lib/postgresql/data \
			${DOCKER_IMAGE} \
			/usr/local/bin/restore-db.sh

run:
	docker run --rm \
		-p 15432:5432 -it \
		-v ${VOLUME_ETOOLS_DATA}:/var/lib/postgresql/data \
		${DOCKER_IMAGE}

stop:
	docker stop ${DOCKER_IMAGE}


shell:
	docker run --rm \
		-it \
		-e DB_DUMP_LOCATION=${DB_DUMP_LOCATION} \
		-v ${VOLUME_ETOOLS_BACKUP}:/tmp/psql_data/ \
		-v ${VOLUME_ETOOLS_DATA}:/var/lib/postgresql/data \
		${DOCKER_IMAGE} \
		/bin/bash
