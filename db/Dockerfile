FROM mdillon/postgis:9.5

RUN mkdir -p /tmp/psql_data/

COPY db1.bz2 /tmp/psql_data/
COPY ./load_db_data.sh /docker-entrypoint-initdb.d/postgis.sh
