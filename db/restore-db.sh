#!/bin/sh


set -e

/usr/lib/postgresql/$PG_MAJOR/bin/pg_ctl -D "$PGDATA" -m fast -w start

echo "*** UPDATING DATABASE ***"
bzcat $DB_DUMP_LOCATION | nice pg_restore -U etoolusr -F t -d etools

echo "*** DATABASE CREATED! ***"

