build:
	docker build \
		-t unicef/etools-db:dev \
		-f Dockerfile .


init:
	docker run --rm -it \
			-e DB_DUMP_LOCATION=/tmp/psql_data/db1.bz2 \
			-v /data/storage/etools-db/dumps:/tmp/psql_data/ \
			-v /data/storage/etools-db/data:/var/lib/postgresql/data \
			unicef/etools-db:dev

run:
	docker run --rm \
		-p 15432:5432 -it \
		-v /data/storage/etools-db/data:/var/lib/postgresql/data \
		unicef/etools-db:dev

