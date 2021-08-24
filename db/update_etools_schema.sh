#!/usr/bin/env bash
# This script should be used everytime eTools ORM changes
#
# It loads local eTools database with provided data,
# re-align Datamart ORM to Etools ORM and produce
# sql files used by Datamart tests.
#
# NOTE: for safety reasosn etools database MUST listn on 15432

set -e

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
PROJECT_DIR="`cd "${CURDIR}/..";pwd`"
DUMP_DIRECTORY="$PROJECT_DIR/src/etools_datamart/apps/multitenant/postgresql"
MODEL_DIR="$PROJECT_DIR/src/etools_datamart/apps/sources/etools/models/"

export DEBUG=${DEBUG:=True}
export PGHOST=${PGHOST:=db-etools}
export PGPORT=${PGPORT:=5432}
export DATABASE_NAME=${DATABASE_NAME:=etools}
export DATABASE_USER=${DATABASE_USER:=postgres}
export DATABASE_PASS=${DATABASE_PASS:=pass}

export BACKUPFILE=${ETOOLS_BACKUP:=2019-04-08-1600.bz2}


help (){
    echo "$0"
    echo " "
    echo "  -o,--only             d=DROP, o=OBFUSCATE, r=RESET_PASSWORD, p=DUMP_PUBLIC, t=DUMP_TENANT, m=MOVE, i=INSPECT, s=SUMMARY, c=CLEAN"
    echo "  -nd,--no-drop         do not recreate database"
    echo "  -no,--no-obfuscate    do not obfuscate sensitive data"
    echo "  -nr,--no-password     do not reset user passwords"
    echo "  -np,--no-dump-public  do not create tests public dump data files"
    echo "  -nt,--no-dump-tenant  do not create tests tenant dump data files"
    echo "  -nm,--no-move         do not move testing data files to source code dir"
    echo "  -ni,--no-inspect      do not inspect schema"
    echo "  -ns,--no-summary      do not display summary infos"
    echo "  -nc,--no-clean        do not clean temporary files"
    echo "  --host                database host"
    echo "  --port                database port"
    echo "  --db-name             database name"
    echo "  --db-user             database username"
    echo "  --db-pass             database password"
    echo "  -h,--help             this help screen"
    echo "  --schemas             Base schema [$BASE_SCHEMAS]"
    echo "  --interactive         interactive mode"
    exit 1
}

DROP=1
OBFUSCATE=1
RESET_PASSWORD=1
DUMP_PUBLIC=1
DUMP_TENANT=1
MOVE=1
SUMMARY=1
CLEAN=1
INSPECT=1
INTERACTIVE=0
BASE_SCHEMAS="uat,libya,chad"
BASE_SCHEMA="uat"

while [[ "$1" != "" ]]; do
case $1 in
    -o|--only)
        [[ "$2" =~ d ]] && DROP=1 || DROP=0
        [[ "$2" =~ o ]] && OBFUSCATE=1 || OBFUSCATE=0
        [[ "$2" =~ r ]] && RESET_PASSWORD=1 || RESET_PASSWORD=0
        [[ "$2" =~ p ]] && DUMP_PUBLIC=1 || DUMP_PUBLIC=0
        [[ "$2" =~ t ]] && DUMP_TENANT=1 || DUMP_TENANT=0
        [[ "$2" =~ m ]] && MOVE=1 || MOVE=0
        [[ "$2" =~ i ]] && INSPECT=1 || INSPECT=0
        [[ "$2" =~ s ]] && SUMMARY=1 || SUMMARY=0
        [[ "$2" =~ c ]] && CLEAN=1 || CLEAN=0
        shift
        shift
        ;;
    --host)
        shift
        PGHOST=$1
        shift
        ;;
    --port)
        shift
        PGPORT=$1
        shift
        ;;
    --db-name)
        shift
        DATABASE_NAME=$1
        shift
        ;;
    --db-user)
        shift
        DATABASE_USER=$1
        shift
        ;;
    --db-pass)
        shift
        DATABASE_PASS=$1
        shift
        ;;
    -nd|--no-drop)
        DROP=0
        shift
        ;;
    -no|--no-obfuscate)
        OBFUSCATE=0
        shift
        ;;
    -np|--no-dump-public)
        DUMP_PUBLIC=0
        shift
        ;;
    -nt|--no-dump-tenant)
        DUMP_TENANT=0
        shift
        ;;
    -nm|--no-move)
        MOVE=0
        shift
        ;;
    -np|--no-password)
        RESET_PASSWORD=0
        shift
        ;;
    -ni|--no-inspect)
        INSPECT=0
        shift
        ;;
    -ns|--no-summary)
        SUMMARY=0
        shift
        ;;
    -nc|--no-clean)
        CLEAN=0
        shift
        ;;
    --schemas)
        shift
        BASE_SCHEMAS=$1
        shift
        ;;
    --interactive)
        INTERACTIVE=1
        shift
        ;;
    -h|--help)
        help
        ;;
    *) echo "unknown option '$1'"
       help
       ;;
esac
done

print(){
    if [[ "$1" == "1" ]]; then
        echo -en "\e[92m+ "
    else
        echo -en "\e[33m- "
    fi
    echo -e "$2\e[0m"
}

echo "Configuration:"
print $DROP             "[d]rop and rebuild database - restore etools db with data from dump file. $BACKUPFILE -> etools.dump -> DB"
print $OBFUSCATE        "[o]bfuscate sensitive data  - obfuscate sensitive data (email, names, phones..)"
print $RESET_PASSWORD   "[r]eset password            - set all user password as 'password' "
print $DUMP_PUBLIC      "[p]ublic schema dump        - dump cleanded data to $CURDIR (public.sqldump)"
print $DUMP_TENANT      "[t]enant schema dump        - dump cleanded data to $CURDIR ([$BASE_SCHEMAS].sql)"
print $MOVE             "[m]ove testing data files   - move dump files to datamart source code"
print $INSPECT          "[i]nspect db and update ORM - inspect db and creates new Models code"
print $SUMMARY          "[s]summary                  - print summary informations"
print $CLEAN            "[c]lean temporary files     - removes temporary files (etools.dump, [$BASE_SCHEMAS].sql, clean.sql, public.sqldump)"
echo  "Connection        ${DATABASE_USER}:${DATABASE_PASS}@${PGHOST}:${PGPORT}/${DATABASE_NAME}"

if [[ "$DROP" = "1" ]];then
  if [[ ! -e ${BACKUPFILE} ]];then
    echo -e "\e[31mERROR: Database backup file '${BACKUPFILE}' not found"
    exit 1
  else
    echo "Database dump:    ${BACKUPFILE}"
  fi
fi
echo
#echo "Confirm ? Type the year that you want to check (4 digits), followed by [ENTER]:"

read -p "Continue? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running..."
else
    echo "Abort..."
    exit 1
fi


function drop(){
    MSG="1.1 Dropping and recreating database ${DATABASE_NAME}"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    dropdb -h ${PGHOST} -p ${PGPORT} --if-exists ${DATABASE_NAME} || exit 1
    createdb -h ${PGHOST} -p ${PGPORT} ${DATABASE_NAME} || exit 1

    if [[ ! -e "$CURDIR/etools.dump" ]];then
        echo "1.2 Unpack database dump"
        bzcat ${BACKUPFILE} > etools.dump
    else
        echo "1.2 datafile not unpacked: 'etools.dump' exists"
    fi

    echo "1.3 Restoring database"

    pg_restore -h ${PGHOST} -p ${PGPORT} \
            --no-owner --role=${DATABASE_USER} \
            --username=${DATABASE_USER} \
            -F c --dbname=${DATABASE_NAME} etools.dump || exit 1

}

function obfuscate(){
    MSG="2.1 remove sensitive data (OBFUSCATE)"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    IFS=,
    for tenant in $BASE_SCHEMAS; do
        cat  clean.tpl.sql | sed "s/_SCHEMA_/${tenant}/" > $CURDIR/clean.sql || exit 1
        psql -h ${PGHOST} -p ${PGPORT} -U ${DATABASE_USER} \
            -qtAX \
            -d ${DATABASE_NAME} \
            -f $CURDIR/clean.sql || exit 1
    done
}

function reset_password(){
    MSG="3.1 - Reset user passwords (RESET_PASSWORD)"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    psql -h ${PGHOST} -p ${PGPORT} -U ${DATABASE_USER} \
        -qtAX \
        -d ${DATABASE_NAME} \
        -c "SET search_path=public;UPDATE auth_user SET password='';" || exit 1

}

function dump_public(){
    MSG="4.1 Dump public schema (DUMP_PUBLIC)"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    pg_dump --inserts -O \
            -d ${DATABASE_NAME} \
            -U ${DATABASE_USER} \
            -n public \
            --format c \
            --blobs \
            --exclude-table-data auth_group_permissions \
            --exclude-table-data auth_permission \
            --exclude-table-data auth_user_user_permissions \
            --exclude-table-data authtoken_* \
            --exclude-table-data celery_* \
            --exclude-table-data django_admin_log \
            --exclude-table-data django_celery_* \
            --exclude-table-data django_migrations \
            --exclude-table-data django_session \
            --exclude-table-data djcelery_* \
            --exclude-table-data drfpasswordless_* \
            --exclude-table-data easy_* \
            --exclude-table-data environment_* \
            --exclude-table-data filer_* \
            --exclude-table-data locations_location \
            --exclude-table-data generic_* \
            --exclude-table-data notification_* \
            --exclude-table-data permissions2_* \
            --exclude-table-data post_office_* \
            --exclude-table-data registration_* \
            --exclude-table-data reversion_* \
            --exclude-table-data social_auth_* \
            --exclude-table-data socialaccount_* \
            --exclude-table-data spatial_* \
            --exclude-table-data tpm_partners_* \
            --exclude-table-data unicef_notification_* \
            --exclude-table-data unicef_snapshot_* \
            --exclude-table-data vision_* \
            --exclude-table-data waffle_* \
            -f $CURDIR/public.sqldump
}

function dump_tenant(){
    MSG="4.2 Dump tenant schema"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    IFS=,
    for tenant in $BASE_SCHEMAS; do
        echo "4.2.1 Dump $tenant"
        pg_dump --inserts -O  -d ${DATABASE_NAME} -U ${DATABASE_USER} \
                --exclude-table-data django_migrations \
                --exclude-table-data django_comments \
                --exclude-table-data django_comment_flags \
                --exclude-table-data django_migrations \
                --exclude-table-data locations_cartodbtable \
                --exclude-table-data locations_locationremaphistory \
                --exclude-table-data reversion_* \
                --exclude-table-data snapshot_* \
                -n $tenant | sed "s/${tenant}/[[schema]]/g" >$CURDIR/tenant_${tenant}.sql
    done
}

function move(){
    MSG="5.x Move dumps needed for tests(MOVE)"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    IFS=,
    COUNTER=1
    for tenant in $BASE_SCHEMAS; do
        if [ -f $CURDIR/tenant_${tenant}.sql ]; then
            echo "5.${COUNTER} Move 'tenant_${tenant}.sql' to ${DUMP_DIRECTORY}/tenant${COUNTER}.sql"
            cp $CURDIR/tenant_${tenant}.sql ${DUMP_DIRECTORY}/tenant${COUNTER}.sql
            COUNTER=$((COUNTER+1))
        fi
    done
    if [ -f $CURDIR/public.sqldump ]; then
        echo "5.${COUNTER} Move 'public.sqldump' to ${DUMP_DIRECTORY}"
        cp $CURDIR/public.sqldump ${DUMP_DIRECTORY}/public.sqldump
    fi


}

function inspect(){
    MSG="6.x Inspect database schema (INSPECT)"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    cd $CURDIR/..
    echo "6.1 Inspect 'public' schema"
    ./manage.py inspectschema --database etools > $MODEL_DIR/public_new.py

    echo "6.2 Inspect 'tenant' schema (${BASE_SCHEMA})"
    ./manage.py inspectschema --database etools --schema=${BASE_SCHEMA} > $MODEL_DIR/tenant_new.py

    echo "6.3 Backup old models"
    mv $MODEL_DIR/public.py $MODEL_DIR/public_old.py
    mv $MODEL_DIR/tenant.py $MODEL_DIR/tenant_old.py

    echo "6.4 Enable new models"
    mv $MODEL_DIR/public_new.py $MODEL_DIR/public.py
    mv $MODEL_DIR/tenant_new.py $MODEL_DIR/tenant.py

    echo "6.5 Checking installation"
    ./manage.py check
    cd $CURDIR
}

function summary(){
    MSG="7.x Summary summary (SUMMARY)"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    echo ""
    echo "================================================================"
    for TABLE in action_points_actionpoint \
                 activities_activity \
                 funds_fundsreservationheader \
                 partners_partnerorganization \
                 partners_intervention \
                 partners_intervention_flat_locations \
                 reports_appliedindicator
    do
        v=`psql -h ${PGHOST} -p ${PGPORT} -U ${DATABASE_USER} \
                -qtAX \
                -d ${DATABASE_NAME} \
                -c "SET search_path=${BASE_SCHEMAS};SELECT COUNT(*) FROM $TABLE;"`
        echo "${TABLE^^} = $v"
        echo $v > $PROJECT_DIR/tests/COUNT_${TABLE^^}

    done
    echo "================================================================"

#    v=`psql -h ${PGHOST} -p ${PGPORT} -U ${DATABASE_USER} \
#            -qtAX \
#            -d ${DATABASE_NAME} \
#            -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM partners_partnerorganization;"`
#    echo "number_of_partnerorganization = $v"
#    echo $v > $PROJECT_DIR/tests/PARTNERORGANIZATION
#
#    v=`psql -h ${PGHOST} -p ${PGPORT} -U ${DATABASE_USER} \
#        -qtAX \
#        -d ${DATABASE_NAME} \
#        -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM partners_intervention;"`
#    echo $v > $PROJECT_DIR/tests/INTERVENTION
#    echo "number_of_intervention = $v"
#
#    v=`psql -h ${PGHOST} -p ${PGPORT} -U ${DATABASE_USER} \
#        -qtAX \
#        -d ${DATABASE_NAME} \
#        -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM activities_activity;"`
#    echo $v > $PROJECT_DIR/tests/ACTIVITIES
#    echo "number_of_activities = $v"
#    echo "================================================================"
}

function clean(){
    MSG="8.x Clean temporary files"
    if [[ "$INTERACTIVE" == "1" ]]; then
        read -p $MSG -n 1 -r; echo
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    cd $CURDIR
    rm -f etools.dump
    rm -f tenant_*.sql
    rm -f clean.sql
    rm -f public.sqldump
}

start=$SECONDS

# 1 - restore from database dump
if [[ "$DROP" == "1" ]]; then
    drop
else
    echo "1.x SKIP Dropping and recreating database (RESTORE)"
fi

if [[ "$OBFUSCATE" == "1" ]]; then
    obfuscate
else
    echo "2.1 SKIP remove sensitive data (OBFUSCATE)"
fi


if [[ "$RESET_PASSWORD" == "1" ]]; then
    reset_password
else
    echo "3.x SKIP Reset user passwords (RESET_PASSWORD)"
fi


if [[ "$DUMP_PUBLIC" == "1" ]]; then
    dump_public
else
    echo "4.x SKIP Dump schemas (DUMP_PUBLIC)"
fi


if [[ "$DUMP_TENANT" == "1" ]]; then
    dump_tenant
else
    echo "4.x SKIP Dump schemas (DUMP_TENANT)"
fi


if [[ "$MOVE" == "1" ]]; then
    move
else
    echo "5.x SKIP Move schemas (MOVE)"
fi


if [[ "$INSPECT" == "1" ]]; then
    inspect
else
    echo "6.x SKIP nspect db and update ORM (INSPECT)"
fi


if [[ "$SUMMARY" == "1" ]]; then
    summary
else
    echo "7.x SKIP Summary summary (SUMMARY)"
fi

if [[ "$CLEAN" == "1" ]]; then
    clean
else
    echo "8.x SKIP Clean temporary files"
fi



end=$SECONDS
duration=$(( end - start ))

echo "Done!!!"
echo "Total of $duration seconds elapsed for process"
