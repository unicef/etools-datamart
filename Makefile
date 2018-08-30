VERSION=2.0.0
BUILDDIR='~build'
PYTHONPATH:=${PWD}/tests/:${PWD}
DBENGINE?=pg
DJANGO?='last'
PG_ETOOLS_PARAMS=-U postgres -p 15432 -h 127.0.0.1

.mkbuilddir:
	mkdir -p ${BUILDDIR}

help:
	echo ""


develop:
	@pipenv install -d
	pre-commit install
	$(MAKE) .init-db


.init-db:
	psql -h 127.0.0.1 -c 'DROP DATABASE IF EXISTS etools_datamart;' -U postgres
	psql -h 127.0.0.1 -c 'CREATE DATABASE etools_datamart;' -U postgres

test:
	pipenv run py.test -v --create-db

lint:
	pipenv run flake8 src/ tests/
	pipenv run isort -rc src/ --check-only
	pipenv run check-manifest

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml .eggs
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src/concurrency/locale -name django.mo | xargs rm -f

fullclean:
	rm -fr .tox .cache
	$(MAKE) clean


sync-etools:
	pg_dump --inserts -O \
		${PG_ETOOLS_PARAMS} -d etools -n public \
		--format c \
		--blobs \
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
		--exclude-table-data vision_* \
		--exclude-table-data waffle_* \
		-f src/etools_datamart/apps/multitenant/postgresql/public.sqldump
	pg_dump --inserts -O -U postgres -p 15432 -d etools -h 127.0.0.1 -n zambia | sed 's/zambia/[[schema]]/g' >src/etools_datamart/apps/multitenant/postgresql/tenant.sql
	ls -aslkG src/etools_datamart/apps/multitenant/postgresql/*.sql*


docs: .mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/ ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
