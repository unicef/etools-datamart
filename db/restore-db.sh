#!/bin/sh


set -e
if [ -n "$DB_DUMP_LOCATION" ];then
    if [ -f "$DB_DUMP_LOCATION" ];then
        echo "*** UPDATING DATABASE ***"
        bzcat $DB_DUMP_LOCATION | nice pg_restore -U etoolusr -F t -d etools
        echo "*** DATABASE CREATED! ***"
    else
        echo "$DB_DUMP_LOCATION not found"
    fi
else
    echo "'DB_DUMP_LOCATION' not set. Nothing to restore"

fi
