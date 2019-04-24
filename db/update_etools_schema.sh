#!/usr/bin/env bash
# This script should be used everytime eTools ORM changes
#
# It loads local eTools database with provided data,
# re-align Datamart ORM to Etools ORM and produce
# sql files used by Datamart tests.
#
# NOTE: for safety reasosn etools database MUST listn on 15432

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
PROJECT_DIR="`cd "${CURDIR}/..";pwd`"
DUMP_DIRECTORY="$PROJECT_DIR/src/etools_datamart/apps/multitenant/postgresql"
MODEL_DIR="$PROJECT_DIR/src/etools_datamart/apps/etools/models/"

export PGHOST=127.0.0.1
export PGPORT=5432
export DATABASE_NAME=etools
export DATABASE_USER=postgres
export DATABASE_PASS=
export BASE_SCHEMA=uat
export BACKUPFILE=2019-04-08-1600.bz2

help (){
    echo "$0"
    echo " "
    echo "  -o,--only             d=DROP, o=OBFUSCATE, r=RESET_PASSWORD, d=DUMP_PUBLIC, m=MOVE, i=INSPECT, s=SUMMARY, c=CLEAN"
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
        [[ "$2" =~ i ]] && SUMMARY=1 || SUMMARY=0
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
    -h|--help)
        help
        ;;
    *) echo "unknown option '$1'"
       help
       ;;
esac
done
echo "Configuration:"
echo "[d]rop and rebuild database  $DROP - restore etools db with data from dump file. db1.bz2 -> etools.dump -> DB"
echo "[o]bfuscate sensitive data   $OBFUSCATE - obfuscate sensitive data (email, names, phones..)"
echo "[r]eset password             $RESET_PASSWORD - set all user password as 'password' "
echo "[p]ublic schema dump         $DUMP_PUBLIC - dump cleanded data to $CURDIR (public.sqldump, tenant.sqldump)"
echo "[t]enant schema dump         $DUMP_TENANT - dump cleanded data to $CURDIR (public.sqldump, tenant.sqldump)"
echo "[m]ove testing data files    $MOVE - move dump files to datamart source code"
echo "[i]nspect db and update ORM  $INSPECT - inspect db and creates new Models code"
echo "[s]summary                   $SUMMARY - print summary informations"
echo "[c]lean temporary files      $CLEAN - removes temporary files (etools.dump, tenant.sql, clean.sql, public.sqldump)"
echo "Connection                 http://${DATABASE_USER}:${DATABASE_PASS}@${PGHOST}:${PGPORT}/${DATABASE_NAME}"
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

# 1 - restore from database dump
if [[ "$DROP" == "1" ]]; then
    echo "1.1 Dropping and recreating database ${DATABASE_NAME}"
    dropdb -h ${PGHOST} -p ${PGPORT} --if-exists ${DATABASE_NAME} || exit 1
    createdb -h ${PGHOST} -p ${PGPORT} ${DATABASE_NAME} || exit 1

    if [ ! -e "$CURDIR/etools.dump" ];then
        echo "1.2 Unpack database dump"
        bzcat ${BACKUPFILE} > etools.dump
    else
        echo "1.2 datafile not unpacked: 'etools.dump' exists"
    fi

    echo "1.3 Restoring database"

    pg_restore -h ${PGHOST} -p ${PGPORT} \
            --no-owner --role=${DATABASE_USER} \
            --username=${DATABASE_USER} \
            --format=tar --dbname=${DATABASE_NAME} etools.dump
else
    echo "1.x SKIP Dropping ans recreating database (RESTORE)"
fi

set -e

if [[ "$OBFUSCATE" == "1" ]]; then
    # 2 - remove sensitive data
    echo "2.1 remove sensitive data (OBFUSCATE)"
    cat  clean.tpl.sql | sed "s/_SCHEMA_/${BASE_SCHEMA}/" > $CURDIR/clean.sql
else
    echo "2.1 SKIP remove sensitive data (OBFUSCATE)"
fi


if [[ "$RESET_PASSWORD" == "1" ]]; then
    # 3 - reset all passwords
    echo "3.1 - Reset user passwords (RESET_PASSWORD)"
    DJANGO_SETTINGS_MODULE=etools_datamart.config.settings \
    PYTHONPATH=$CURDIR/../src  \

    psql -h ${PGHOST} -p ${PGPORT} \
        -qtAX \
        -d ${DATABASE_NAME} \
        -c "SET search_path=public;UPDATE auth_user SET password='';"
#    django-admin shell -c \
#        "from etools_datamart.apps.etools.models import AuthUser; \
#        [u.set_password('password') for u in AuthUser.objects.all()]"
else
    echo "3.x SKIP Reset user passwords (RESET_PASSWORD)"
fi


if [[ "$DUMP_PUBLIC" == "1" ]]; then
    # 4 - Dump data
    echo "4.1 Dump public schema (DUMP_PUBLIC)"
    pg_dump --inserts -O \
            -d ${DATABASE_NAME} \
            -n public \
            --format c \
            --blobs \
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
            --exclude-table-data social_account_* \
            --exclude-table-data spatial_* \
            --exclude-table-data tpm_partners_* \
            --exclude-table-data unicef_notification_* \
            --exclude-table-data unicef_snapshot_* \
            --exclude-table-data vision_* \
            --exclude-table-data waffle_* \
            -f $CURDIR/public.sqldump

else
    echo "4.x SKIP Dump schemas (DUMP_PUBLIC)"
fi

if [[ "$DUMP_TENANT" == "1" ]]; then
    echo "4.2 Dump tenant schema"

    pg_dump --inserts -O  -d ${DATABASE_NAME} \
            --exclude-table-data django_migrations \
            --exclude-table-data django_comments \
            --exclude-table-data django_comment_flags \
            --exclude-table-data locations_cartodbtable \
            --exclude-table-data locations_locationremaphistory \
            -n ${BASE_SCHEMA} | sed "s/${BASE_SCHEMA}/[[schema]]/g" >$CURDIR/tenant.sql
else
    echo "4.x SKIP Dump schemas (DUMP_TENANT)"
fi


if [[ "$MOVE" == "1" ]]; then
    echo "5.x Move dumps needed for tests(MOVE)"
    if [ -f $CURDIR/tenant.sql ]; then
        echo "5.1 Move 'tenant.sql' to ${DUMP_DIRECTORY}"
        cp $CURDIR/tenant.sql ${DUMP_DIRECTORY}
    fi
    if [ -f $CURDIR/public.sqldump ]; then
        echo "5.2 Move 'public.sqldump' to ${DUMP_DIRECTORY}"
        cp $CURDIR/public.sqldump ${DUMP_DIRECTORY}
    fi
else
    echo "5.x SKIP Move schemas (MOVE)"
fi


if [[ "$INSPECT" == "1" ]]; then
    echo "6.x Inspect database schema (INSPECT)"
    cd $CURDIR/..
    echo "6.1 Inspect 'public' schema"
    ./manage.py inspectschema --database etools  > $CURDIR/../src/etools_datamart/apps/etools/models/public_new.py

    echo "6.2 Inspect 'tenant' schema (${BASE_SCHEMA})"
    ./manage.py inspectschema --database etools --schema=${BASE_SCHEMA} > $CURDIR/../src/etools_datamart/apps/etools/models/tenant_new.py

    echo "6.3 Backup old models"
    mv $MODEL_DIR/public.py $MODEL_DIR/public_old.py
    mv $MODEL_DIR/tenant.py $MODEL_DIR/tenant_old.py

    echo "6.4 Enable new models"
    mv $MODEL_DIR/public_new.py $MODEL_DIR/public.py
    mv $MODEL_DIR/tenant_new.py $MODEL_DIR/tenant.py
    echo "6.5 Checking installation"
    ./manage.py check
    cd $CURDIR
fi

if [[ "$SUMMARY" == "1" ]]; then
    echo "7.x Summary summary (SUMMARY)"
    echo "================================================================"
#    echo "Update your conftest.py fixtures with following values:"
    v=`psql -h ${PGHOST} -p ${PGPORT} \
            -qtAX \
            -d ${DATABASE_NAME} \
            -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM partners_partnerorganization;"`
    echo "number_of_partnerorganization = $v"
    echo $v > $PROJECT_DIR/tests/PARTNERORGANIZATION

    v=`psql -h ${PGHOST} -p ${PGPORT} \
        -qtAX \
        -d ${DATABASE_NAME} \
        -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM partners_intervention;"`
    echo $v > $PROJECT_DIR/tests/INTERVENTION
    echo "number_of_intervention = $v"
    echo "================================================================"

    v=`psql -h ${PGHOST} -p ${PGPORT} \
        -qtAX \
        -d ${DATABASE_NAME} \
        -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM activities_activity;"`
    echo $v > $PROJECT_DIR/tests/ACTIVITIES
    echo "number_of_activities = $v"
    echo "================================================================"
else
    echo "7.x SKIP Summary summary (SUMMARY)"
fi

if [[ "$CLEAN" == "1" ]]; then
    echo "8.x Clean temporary files"
    cd $CURDIR
    rm -f etools.dump
    rm -f tenant.sql
    rm -f clean.sql
    rm -f public.sqldump
else
    echo "8.x SKIP Clean temporary files"
fi

echo "Done!!!"
