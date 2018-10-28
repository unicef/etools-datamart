#!/usr/bin/env bash

set -eo pipefail

PG_ETOOLS_PARAMS=$@
BASE_SCHEMA=zambia

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $CURDIR

cat  clean.tpl.sql | sed "s/_SCHEMA_/${BASE_SCHEMA}/" > $CURDIR/clean.sql
psql ${PG_ETOOLS_PARAMS} -d etools -f $CURDIR/clean.sql


pg_dump --inserts -O \
		${PG_ETOOLS_PARAMS} -d etools \
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

pg_dump --inserts -O ${PG_ETOOLS_PARAMS} -d etools \
    -n ${BASE_SCHEMA} | sed "s/${BASE_SCHEMA}/[[schema]]/g" >$CURDIR/tenant.sql

ls -alGfh public.sqldump
ls -alGfh tenant.sql

rm $CURDIR/clean.sql
