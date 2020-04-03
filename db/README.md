## Datamart eTools database 

This directory contains files and scripts needed to:

- extract data from eTools backup
- create .sql files for test data
- builds docker image for the eTools test database

- keep database updated to eTools schema

**Read Makefile to check configuration variables. Consider your changes reading this file**

### Build initial eTools test database :

- get a .bz2 backup file from etools and name it `db2.bz2`
- copy somewhere and set `VOLUME_BACKUP` environment variable.
    (it must point to the directory)
- run `make build init`

### Run migrations:

To keep test database updated without the need to rebuild it from a backup, you can run migrations
using a eTools docker image against the test database.
Simply run:

    - make run
    - DATABASE_URL_ETOOLS=postgis://postgres:@127.0.0.1:5432/etools migrate-etools.sh`
    - make stop
