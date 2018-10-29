#!/usr/bin/env bash
# This script should be used everytime eTools ORM changes
#
# It will re-align Datamart ORM to Etools ORM and produce
# sql files used by Datamart tests
#
# NOTE: for safety reasosn etools database MUST listn on 15432

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DUMP_DIRECTORY="$CURDIR/../src/etools_datamart/apps/multitenant/postgresql"

export PGHOST=127.0.0.1
export PGPORT=15432
export DATABASE_NAME=etools
export DATABASE_USER=etoolusr
export BASE_SCHEMA=kenya

help (){
    echo "$0"
    echo " "
    echo "  -o,--only           r=RESTORE, c=OBFUSCATE, p=PASSWORD, d=DUMP, m=MOVE, i=INFO, c=CLEAN"
    echo "  -nr,--no-restore    do not recreate database"
    echo "  -no,--no-obfuscate  do not obfuscate sensitive data"
    echo "  -np,--no-password   do not reset user passwords"
    echo "  -nd,--no-dump       do not create tests dump data files"
    echo "  -nm,--no-move       do not move testing data files to source code dir"
    echo "  -ni,--no-info       do not display summary info"
    echo "  -nc,--no-clean      do not clean temporary files"
    echo "  -h,--help           this help screen"
    exit 1
}

RESTORE=1
OBFUSCATE=1
DUMP=1
MOVE=1
PASSWORD=1
INFO=1
CLEAN=1

while [ "$1" != "" ]; do
case $1 in
    -o|--only)
        [[ "$2" =~ r ]] && RESTORE=1 || RESTORE=0
        [[ "$2" =~ c ]] && OBFUSCATE=1 || OBFUSCATE=0
        [[ "$2" =~ d ]] && DUMP=1 || DUMP=0
        [[ "$2" =~ m ]] && MOVE=1 || MOVE=0
        [[ "$2" =~ p ]] && PASSWORD=1 || PASSWORD=0
        [[ "$2" =~ i ]] && INFO=1 || INFO=0
        [[ "$2" =~ c ]] && CLEAN=1 || CLEAN=0
        shift
        shift
        ;;
    -nr|--no-restore)
        RESTORE=0
        shift
        ;;
    -no|--no-obfuscate)
        OBFUSCATE=0
        shift
        ;;
    -nd|--no-dump)
        DUMP=0
        shift
        ;;
    -nm|--no-move)
        MOVE=0
        shift
        ;;
    -np|--no-password)
        PASSWORD=0
        shift
        ;;
    -ni|--no-info)
        INFO=0
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

echo "recreate database        $RESTORE"
echo "obfuscate sensitive data $OBFUSCATE"
echo "reset user passwords     $PASSWORD"
echo "create tests data files  $DUMP"
echo "move testing data files  $MOVE"
echo "clean temporary files    $CLEAN"

# 1 - restore from database dump

if [ "$RESTORE" == "1" ]; then
    echo "1.1 Dropping ans recreating database ${DATABASE_NAME}"
    dropdb -h ${PGHOST} -p ${PGPORT} --if-exists ${DATABASE_NAME}
    createdb -h ${PGHOST} -p ${PGPORT} ${DATABASE_NAME}

    if [ ! -e "$CURDIR/etools.dump" ];then
        echo "1.2 Unpack database dump"
        bzcat db1.bz2 > etools.dump
    else
        echo "1.2 datafile not unpacked: 'etools.dump' exists"
    fi

    echo "1.3 Restoring database"

    pg_restore -h ${PGHOST} -p ${PGPORT} \
            --no-owner --role=postgresql \
            --username=${DATABASE_USER} --format=tar --dbname=${DATABASE_NAME} etools.dump

    rm -f etools.dump etools.dump.list _etools.dump.list
else
    echo "1.x SKIP Dropping ans recreating database (RESTORE)"
fi


if [ "$OBFUSCATE" == "1" ]; then
    # 2 - remove sensitive data
    echo "2.1 remove sensitive data (OBFUSCATE)"
    cat  clean.tpl.sql | sed "s/_SCHEMA_/${BASE_SCHEMA}/" > $CURDIR/clean.sql
else
    echo "2.1 SKIP remove sensitive data (OBFUSCATE)"
fi


if [ "$PASSWORD" == "1" ]; then
    # 3 - reset all passwords
    echo "3.1 - Reset user passwords (PASSWORD)"
    DJANGO_SETTINGS_MODULE=etools_datamart.config.settings \
    PYTHONPATH=$CURDIR/../src  \
    django-admin shell -c \
        "from etools_datamart.apps.etools.models import AuthUser; \
        [u.set_password('password') for u in AuthUser.objects.filter(id__lt=50)]"
else
    echo "3.x SKIP Reset user passwords (PASSWORD)"
fi


if [ "$DUMP" == "1" ]; then
    # 4 - Dump data
    echo "4.1 Dump public schema (DUMP)"
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
            --exclude-table-data purchase_order_* \
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

    echo "4.2 Dump tenant schema"

    pg_dump --inserts -O  -d ${DATABASE_NAME} \
        -n ${BASE_SCHEMA} | sed "s/${BASE_SCHEMA}/[[schema]]/g" >$CURDIR/tenant.sql
else
    echo "4.x SKIP Dump schemas (DUMP)"
fi


if [ "$MOVE" == "1" ]; then
    # 5 - MOVE dump files to code
    echo "5.1 - MOVE 'tenant.sql' to ${DUMP_DIRECTORY}"
    cp $CURDIR/tenant.sql ${DUMP_DIRECTORY}
    echo "5.2 - MOVE 'public.sqldump' to ${DUMP_DIRECTORY}"
    cp $CURDIR/public.sqldump ${DUMP_DIRECTORY}
else
    echo "5.x SKIP Move schemas (MOVE)"
fi


if [ "$INFO" == "1" ]; then
    echo "6.x Summary info (INFO)"
    echo "================================================================"
    echo "Update your conftest.py fixtures with following values:"
    v=`psql -h ${PGHOST} -p ${PGPORT} \
            -qtAX \
            -d ${DATABASE_NAME} \
            -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM partners_partnerorganization;"`
    echo "number_of_partnerorganization = $v"

    v=`psql -h ${PGHOST} -p ${PGPORT} \
        -qtAX \
        -d ${DATABASE_NAME} \
        -c "SET search_path=${BASE_SCHEMA};SELECT COUNT(*) FROM partners_intervention;"`
    echo "number_of_intervention = $v"
    echo ""
    echo "Remember to update eTools ORM running"
    echo ""
    echo "./manage.py inspectschema --database etools  > src/etools_datamart/apps/etools/models/public_new.py"
    echo "./manage.py inspectschema --database etools --schema=bolivia > src/etools_datamart/apps/etools/models/tenant_new.py"
    echo "================================================================"
else
    echo "6.x SKIP Summary info (INFO)"
fi

if [ "$CLEAN" == "1" ]; then
    echo "7.x Clean temporary files"
    rm -f etools.dump
else
    echo "7.x SKIP Clean temporary files"
fi

echo "Done!!!"
