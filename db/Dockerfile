FROM mdillon/postgis:9.6

#RUN mkdir -p /tmp/psql_data/

#COPY db1.bz2 /tmp/psql_data/
COPY ./load_db_data.sh /docker-entrypoint-initdb.d/load_db_data.sh
COPY restore-db.sh /usr/local/bin/restore-db.sh
ENV POSTGRES_DB etools
ENV POSTGRES_USER etoolusr
ENV DB_DUMP_LOCATION ""
