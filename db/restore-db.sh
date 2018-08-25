#!/bin/sh


set -e
if [ -n "$DB_DUMP_LOCATION" ];then
    if [ -f "$DB_DUMP_LOCATION" ];then
        echo "*** UPDATING DATABASE ***"
        su postgres -c "/usr/lib/postgresql/$PG_MAJOR/bin/pg_ctl -D '$PGDATA' -m fast -w start"
        bzcat $DB_DUMP_LOCATION | nice pg_restore -U etoolusr -F t -d etools
#        su postgres -c psql <<- 'EOSQL'
#        CREATE ROLE etoolusr WITH superuser login;
#        CREATE DATABASE etools;
#        GRANT ALL PRIVILEGES ON DATABASE etools TO etoolusr;
#EOSQL
#
        echo "*** DATABASE CREATED! ***"
    else
        echo "$DB_DUMP_LOCATION not found"
    fi
else
    echo "'DB_DUMP_LOCATION' not set. Nothing to restore"

fi
