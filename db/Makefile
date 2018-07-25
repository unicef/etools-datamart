build:
	docker build \
		-t unicef/etools-db:dev \
		-f Dockerfile .


clean:
	docker rmi unicef/etools-db:dev

restore:
	docker run --rm -it \
			-e DB_DUMP_LOCATION=/tmp/psql_data/db1.bz2 \
			-v /data/storage/etools-db/dumps:/tmp/psql_data/ \
			-v /data/storage/etools-db/data:/var/lib/postgresql/data \
			unicef/etools-db:dev \
			restore-db.sh

run:
	docker run --rm \
		-p 15432:5432 -it \
		-v /data/storage/etools-db/data:/var/lib/postgresql/data \
		unicef/etools-db:dev


shell:
	docker run --rm \
		-p 15432:5432 -it \
			-e DB_DUMP_LOCATION=/tmp/psql_data/db1.bz2 \
			-v /data/storage/etools-db/dumps:/tmp/psql_data/ \
		-v /data/storage/etools-db/data:/var/lib/postgresql/data \
		unicef/etools-db:dev \
		/bin/bash

